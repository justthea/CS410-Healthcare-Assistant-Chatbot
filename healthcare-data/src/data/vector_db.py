import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    Float,
    Index,
    Integer,
    String,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy.types import UserDefinedType

from .fda_client import FDAClient


class VECTOR(UserDefinedType):
    """Custom VECTOR type for PostgreSQL"""

    cache_ok = True

    def __init__(self, dim):
        self.dim = dim

    def get_col_spec(self):
        return f"vector({self.dim})"


Base = declarative_base()


class MedicationCache(Base):
    __tablename__ = "medication_cache"
    __table_args__ = (
        UniqueConstraint("brand_name", "generic_name"),
        Index(
            "idx_medication_cache_embedding", "embedding", postgresql_using="ivfflat"
        ),
        {"schema": "health"},
    )

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    brand_name = Column(String, nullable=False)
    generic_name = Column(String, nullable=False)
    indications = Column(String)
    embedding = Column(VECTOR(384))
    raw_data = Column(JSONB)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class QueryHistory(Base):
    __tablename__ = "query_history"
    __table_args__ = (
        Index("idx_query_history_embedding", "embedding", postgresql_using="ivfflat"),
        {"schema": "health"},
    )

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    query_text = Column(String, nullable=False)
    embedding = Column(VECTOR(384))
    results_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())


class SearchResult(Base):
    __tablename__ = "search_results"
    __table_args__ = (
        Index("idx_search_results_query", "query_id"),
        {"schema": "health"},
    )

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    query_id = Column(UUID, nullable=False)
    medication_id = Column(UUID, nullable=False)
    similarity_score = Column(Float)
    rank = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())


class HealthcareVectorDB:
    def __init__(self):
        load_dotenv()
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.fda_client = FDAClient()

        # Setup database connection
        self.db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        self.engine = create_engine(self.db_url)
        self.Session = sessionmaker(bind=self.engine)

        # Initialize database on startup
        self.setup_vector_extensions()

    def setup_vector_extensions(self):
        """Set up PostgreSQL vector extensions and create tables"""
        try:
            with self.engine.connect() as conn:
                # Create extensions
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto;"))

                # Create schema
                conn.execute(text("CREATE SCHEMA IF NOT EXISTS health;"))

                # Set search path
                conn.execute(text("SET search_path TO health, public;"))

                # Create vector similarity function
                conn.execute(
                    text("""
                    CREATE OR REPLACE FUNCTION health.cosine_similarity(a vector, b vector) 
                    RETURNS float AS $$
                    BEGIN
                        RETURN 1 - (a <=> b);
                    END;
                    $$ LANGUAGE plpgsql IMMUTABLE STRICT PARALLEL SAFE;
                """)
                )

                conn.commit()

            # Create tables using SQLAlchemy ORM
            Base.metadata.schema = "health"
            Base.metadata.create_all(self.engine)

        except Exception as e:
            print(f"Error setting up vector database: {str(e)}")
            raise

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using sentence transformer"""
        embedding = self.model.encode(text)
        return embedding.tolist()

    def cache_medication(self, medication: Dict) -> Optional[MedicationCache]:
        """Store medication data and its embedding in the cache"""
        try:
            session = self.Session()

            # Generate embedding
            text_to_embed = f"{medication['brand_name']} {medication['generic_name']} {medication['indications']}"
            embedding = self.generate_embedding(text_to_embed)

            # Check if medication already exists
            existing = (
                session.query(MedicationCache)
                .filter_by(
                    brand_name=medication["brand_name"],
                    generic_name=medication["generic_name"],
                )
                .first()
            )

            if existing:
                # Update existing record
                existing.indications = medication["indications"]
                existing.embedding = embedding
                existing.raw_data = medication
                existing.updated_at = datetime.now()
                cache_entry = existing
            else:
                # Create new record
                cache_entry = MedicationCache(
                    id=uuid.uuid4(),
                    brand_name=medication["brand_name"],
                    generic_name=medication["generic_name"],
                    indications=medication["indications"],
                    embedding=embedding,
                    raw_data=medication,
                )
                session.add(cache_entry)

            session.commit()
            return cache_entry

        except Exception as e:
            print(f"Error caching medication: {str(e)}")
            session.rollback()
            return None
        finally:
            session.close()

    def find_similar_medications(
        self, query_text: str, limit: int = 5
    ) -> List[Tuple[Dict, float]]:
        """Find similar medications using vector similarity"""
        try:
            session = self.Session()

            # Generate query embedding
            query_embedding = self.generate_embedding(query_text)
            embedding_str = f"[{','.join(map(str, query_embedding))}]"

            # Store query history
            query_record = QueryHistory(
                query_text=query_text, embedding=query_embedding
            )
            session.add(query_record)
            session.flush()

            # Check if we have any medications in cache
            count = session.query(MedicationCache).count()
            print(f"Found {count} medications in cache")

            # Use raw SQL with direct embedding string and lower threshold
            similar_meds = session.execute(
                text(f"""
                    WITH similarity_scores AS (
                        SELECT 
                            m.id as medication_id,
                            m.raw_data,
                            (1 - (m.embedding <=> '{embedding_str}'::vector)) as similarity
                        FROM health.medication_cache m
                        ORDER BY similarity DESC
                        LIMIT :limit
                    )
                    SELECT medication_id, raw_data, similarity, 
                           (SELECT COUNT(*) FROM health.medication_cache) as total_meds
                    FROM similarity_scores
                    WHERE similarity > :threshold;
                """),
                {
                    "threshold": 0.3,  # Lower threshold for better matches
                    "limit": limit,
                },
            ).fetchall()

            # Print detailed debug info
            if similar_meds:
                print("\nSimilarity scores:")
                for _, med, score, _ in similar_meds:
                    print(f"- {med['brand_name']}: {score:.3f}")
            else:
                print("No medications above similarity threshold")

            # Record search results
            for rank, (med_id, med_data, similarity, _) in enumerate(similar_meds, 1):
                result = SearchResult(
                    query_id=query_record.id,
                    medication_id=med_id,  # Use the actual medication_id from the database
                    similarity_score=similarity,
                    rank=rank,
                )
                session.add(result)

            query_record.results_count = len(similar_meds)
            session.commit()

            # Return just the medication and similarity score
            return [(med, sim) for _, med, sim, _ in similar_meds]

        except Exception as e:
            print(f"Error finding similar medications: {str(e)}")
            session.rollback()
            return []
        finally:
            session.close()
