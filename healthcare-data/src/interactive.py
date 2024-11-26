import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from src.data.fda_client import FDAClient
from src.data.vector_db import HealthcareVectorDB


async def process_query(query: str):
    """Process a user query and return medication recommendations"""
    try:
        # Initialize clients
        vector_db = HealthcareVectorDB()
        fda_client = FDAClient()

        # First try vector similarity search
        print("\nSearching cached medications...")
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
            medications = fda_client.search_medications([query])

            if medications:
                print("\nRecommended Medications (from FDA):")
                print("-" * 50)

                # Cache medications before displaying
                for med in medications:
                    vector_db.cache_medication(med)

                    print(f"\nMedication: {med['brand_name']}")
                    print(f"Generic Name: {med['generic_name']}")
                    print(f"Indications: {med['indications'][:200]}...")
                    print(f"Warnings: {med['warnings'][:200]}...")
                    print("-" * 30)
            else:
                print("\nNo medications found for your query.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


async def interactive_session():
    """Run interactive chat session"""
    print("Welcome to the Healthcare Information Assistant!")
    print("Enter 'quit' to exit the program.")

    while True:
        # Get user input
        query = input("\nPlease describe your symptoms: ").strip()

        if query.lower() == "quit":
            break

        # Process query and get recommendations
        await process_query(query)

        print(
            "\nDisclaimer: These recommendations are for informational purposes only."
        )
        print(
            "Always consult with a healthcare professional before taking any medication."
        )


if __name__ == "__main__":
    asyncio.run(interactive_session())
