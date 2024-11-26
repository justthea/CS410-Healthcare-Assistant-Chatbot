import os
from typing import Dict, List
from urllib.parse import quote

import requests
from dotenv import load_dotenv


class FDAClient:
    """Client for interacting with OpenFDA API"""

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("FDA_API_KEY")
        self.base_url = "https://api.fda.gov/drug"

        if not self.api_key:
            raise ValueError("FDA_API_KEY not found in environment variables")

    def search_medications(self, symptoms: List[str], limit: int = 5) -> List[Dict]:
        """Search medications based on symptoms"""
        try:
            # Convert symptoms list to search query and URL encode
            search_terms = " AND ".join(quote(term) for term in symptoms)

            url = f"{self.base_url}/label.json"
            params = {
                "api_key": self.api_key,
                "search": f'indications_and_usage:"{search_terms}"',
                "limit": limit,
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            results = response.json().get("results", [])

            # Format the response
            medications = []
            for result in results:
                medication = {
                    "brand_name": result.get("openfda", {}).get(
                        "brand_name", ["Unknown"]
                    )[0],
                    "generic_name": result.get("openfda", {}).get(
                        "generic_name", ["Unknown"]
                    )[0],
                    "indications": result.get(
                        "indications_and_usage", ["No indication available"]
                    )[0],
                    "warnings": result.get("warnings", ["No warnings available"])[0],
                    "dosage": result.get(
                        "dosage_and_administration", ["No dosage information available"]
                    )[0],
                }
                medications.append(medication)

            return medications

        except requests.exceptions.RequestException as e:
            print(f"Error querying OpenFDA API: {str(e)}")
            return []

    def get_drug_interactions(self, drug_name: str) -> List[str]:
        """Get drug interactions for a specific medication"""
        try:
            url = f"{self.base_url}/label.json"
            params = {
                "api_key": self.api_key,
                "search": f'openfda.brand_name:"{drug_name}" OR openfda.generic_name:"{drug_name}"',
                "limit": 1,
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            results = response.json().get("results", [])
            if results:
                return results[0].get(
                    "drug_interactions", ["No interaction information available"]
                )
            return ["No interaction information available"]

        except requests.exceptions.RequestException as e:
            print(f"Error querying OpenFDA API: {str(e)}")
            return ["Error retrieving interaction information"]
