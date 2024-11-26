import os
import sys

import psycopg2
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from src.data.vector_db import Base


def check_postgres_connection():
    """Check if PostgreSQL is running and database exists"""
    print("Checking PostgreSQL connection...")

    try:
        load_dotenv()
        db_params = {
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
        }

        # First try connecting to PostgreSQL server
        conn = psycopg2.connect(**db_params, database="postgres")
        conn.close()
        print("Successfully connected to PostgreSQL server")

        # Now check if our database exists
        db_name = os.getenv("DB_NAME")
        try:
            conn = psycopg2.connect(**db_params, database=db_name)
            conn.close()
            print(f"Database '{db_name}' exists")
            return True
        except psycopg2.OperationalError:
            # Database doesn't exist, create it
            print(f"Database '{db_name}' not found, creating...")
            conn = psycopg2.connect(**db_params, database="postgres")
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute(f"CREATE DATABASE {db_name}")
            cur.close()
            conn.close()
            print(f"Created database '{db_name}'")
            return True

    except Exception as e:
        print(f"PostgreSQL error: {str(e)}")
        print("\nPlease ensure that:")
        print("1. PostgreSQL is installed and running")
        print("2. Database credentials in .env are correct")
        print("3. PostgreSQL is accepting connections")
        return False


def verify_api_access():
    """Verify access to OpenFDA API"""
    print("\nVerifying OpenFDA API access...")

    try:
        api_key = os.getenv("FDA_API_KEY")
        if not api_key:
            raise ValueError("FDA_API_KEY not found in environment variables")

        test_url = f"https://api.fda.gov/drug/label.json?api_key={api_key}&limit=1"
        response = requests.get(test_url)

        if response.status_code == 200:
            print("Successfully connected to OpenFDA API")
            return True
        else:
            print(f"Error accessing OpenFDA API: {response.status_code}")
            return False

    except Exception as e:
        print(f"Error verifying API access: {str(e)}")
        return False


def setup_vector_database():
    """Set up vector database using SQLAlchemy ORM"""
    print("\nSetting up vector database...")
    try:
        db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        engine = create_engine(db_url)

        with engine.connect() as conn:
            # Create extensions
            print("Setting up PostgreSQL extensions...")
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto;"))

            # Create schema
            print("Creating schema...")
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS health;"))

            # Set search path
            conn.execute(text("SET search_path TO health, public;"))

            # Drop existing function if it exists
            print("Setting up vector similarity function...")
            conn.execute(
                text("""
                DROP FUNCTION IF EXISTS health.cosine_similarity(vector, vector);
                DROP FUNCTION IF EXISTS cosine_similarity(vector, vector);
            """)
            )

            # Create vector similarity function in health schema
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

            # Create indexes
            print("Creating indexes...")
            conn.execute(
                text("""
                CREATE INDEX IF NOT EXISTS idx_medication_cache_embedding 
                ON health.medication_cache USING ivfflat (embedding vector_cosine_ops)
                WITH (lists = 100);  -- Adjust based on your data size
            """)
            )

            # Verify function exists
            print("Verifying setup...")
            result = conn.execute(
                text("""
                SELECT EXISTS (
                    SELECT 1 
                    FROM pg_proc 
                    WHERE proname = 'cosine_similarity'
                );
            """)
            ).scalar()

            if not result:
                raise Exception("Cosine similarity function was not created properly")

            conn.commit()

        # Create tables using SQLAlchemy ORM
        print("Creating tables...")
        Base.metadata.schema = "health"
        Base.metadata.create_all(engine)

        print("Database setup complete")
        return True

    except Exception as e:
        print(f"Error setting up vector database: {str(e)}")
        return False


def check_vector_extension():
    """Check if PostgreSQL vector extension is available"""
    print("\nChecking PostgreSQL vector extension...")
    try:
        db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        engine = create_engine(db_url)

        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM pg_available_extensions WHERE name = 'vector'")
            ).fetchone()
            if result:
                print("Vector extension is available")
                return True
            else:
                print("ERROR: Vector extension is not available")
                print("Please install the PostgreSQL vector extension:")
                return False

    except Exception as e:
        print(f"Error checking vector extension: {str(e)}")
        return False


def main():
    """Main setup function that verifies all components"""
    try:
        print("Starting setup...\n")

        # Step 1: Check PostgreSQL
        if not check_postgres_connection():
            print("\nERROR: PostgreSQL setup failed")
            sys.exit(1)

        # Step 2: Check vector extension
        if not check_vector_extension():
            print("\nERROR: PostgreSQL vector extension not available")
            sys.exit(1)

        # Step 3: Verify API access
        if not verify_api_access():
            print("\nERROR: Unable to access OpenFDA API")
            sys.exit(1)

        # Step 4: Setup vector database
        if not setup_vector_database():
            print("\nERROR: Unable to set up vector database")
            sys.exit(1)

        print("\nSetup completed successfully!")

    except Exception as e:
        print(f"\nError during setup: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
