import asyncio
import os
import sys
from urllib.parse import quote

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.fda_client import FDAClient
from src.data.vector_db import HealthcareVectorDB


async def process_query(query: str):
    """Process a user query and return medication recommendations"""
    try:
        # Initialize clients
        vector_db = HealthcareVectorDB()
        fda_client = FDAClient()

        print(f"Processing query: {query}")

        # First try vector similarity search
        print("Searching cached medications...")
        similar_results = vector_db.find_similar_medications(query)

        if similar_results:
            print("\nRecommended Medications (from cache):")
            print("-" * 50)
            for result in similar_results:
                medication = result[0]  # The medication data
                similarity = result[1]  # The similarity score

                print(f"\nMedication: {medication['brand_name']}")
                print(f"Generic Name: {medication['generic_name']}")
                print(f"Similarity Score: {similarity:.2f}")
                print(f"Indications: {medication['indications'][:200]}...")
                print(f"Warnings: {medication['warnings'][:200]}...")
                print("-" * 30)
        else:
            # If no cached results, query FDA directly
            print("\nNo cached results found, querying FDA API...")
            # URL encode the query
            encoded_query = quote(query)
            medications = fda_client.search_medications([encoded_query])

            if medications:
                print("\nRecommended Medications (from FDA):")
                print("-" * 50)

                # Cache medications before displaying
                cached_meds = []
                for med in medications:
                    cached_entry = vector_db.cache_medication(med)
                    if cached_entry:
                        cached_meds.append(med)

                # Now try similarity search again with cached data
                similar_results = vector_db.find_similar_medications(query)

                if similar_results:
                    print("\nRecommended Medications (from newly cached data):")
                    for result in similar_results:
                        medication = result[0]
                        similarity = result[1]
                        print(f"\nMedication: {medication['brand_name']}")
                        print(f"Generic Name: {medication['generic_name']}")
                        print(f"Similarity Score: {similarity:.2f}")
                        print(f"Indications: {medication['indications'][:200]}...")
                        print(f"Warnings: {medication['warnings'][:200]}...")
                        print("-" * 30)
                else:
                    # Fallback to displaying FDA results directly
                    for med in medications:
                        print(f"\nMedication: {med['brand_name']}")
                        print(f"Generic Name: {med['generic_name']}")
                        print(f"Indications: {med['indications'][:200]}...")
                        print(f"Warnings: {med['warnings'][:200]}...")
                        print("-" * 30)
            else:
                print("\nNo medications found for your query.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise


async def main():
    """Main function to demonstrate medication search"""
    print("Medical Assistant Started")
    print("-" * 50)

    try:
        # Example queries with URL encoding
        queries = [
            "migraine",
            "drowsiness",
            "seasonal allergies",
        ]

        for query in queries:
            print(f"\nProcessing example query: '{query}'")
            await process_query(query)
            print("\n" + "=" * 50)

    except Exception as e:
        print(f"Error in main: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    print("Starting Medical Assistant...")
    asyncio.run(main())
