import os
import logging
import requests
from config.config import get_env

# === Logging Setup ===
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class HarvestAPI:
    """
    A client to interact with the Harvest API to search for LinkedIn-like profiles.

    Loads the API key from environment variables and supports optional filters
    like company, school, and location during the search.
    """
    
    BASE_URL = "https://api.harvest-api.com/linkedin/profile-search"

    def __init__(self):
        # Load API key from environment variable
        self.api_key = get_env("HARVEST_API_KEY", required=True)

    def search_profiles(
        self,
        name: str,
        current_company: str = None,
        past_company: str = None,
        school: str = None,
        location: str = None,
        page: int = 1,
        limit: int = 10
    ):
        """
        Calls the Harvest API to search for profiles based on provided filters.

        Args:
            name (str): Name of the person to search.
            current_company (str, optional): Filter by current company.
            past_company (str, optional): Filter by past company.
            school (str, optional): Filter by school.
            location (str, optional): Filter by location.
            page (int, optional): Pagination page number. Default is 1.
            limit (int, optional): How many results to display (not enforced by API).

        Returns:
            dict: Parsed JSON response from the Harvest API.

        Raises:
            requests.HTTPError: If the request fails (non-2xx status).
        """
        params = {
            "search": name,
            "page": page
        }

        # Add optional filters to the query if provided
        if current_company:
            params["currentCompany"] = current_company
        if past_company:
            params["pastCompany"] = past_company
        if school:
            params["school"] = school
        if location:
            params["location"] = location

        headers = {
            "x-api-key": self.api_key,  # Primary authentication header
            "Authorization": f"Bearer {self.api_key}",  # Just in case API uses this style
            "Accept": "application/json"
        }

        logger.info(f"Sending request to Harvest API with parameters: {params}")

        try:
            response = requests.get(
                self.BASE_URL,
                params=params,
                headers=headers,
                timeout=30
            )
            logger.info(f"Harvest API response status: {response.status_code}")
            response.raise_for_status()

            if response.content:
                return response.json()
            else:
                logger.warning("Harvest API returned empty response body.")
                return {}

        except requests.RequestException as e:
            logger.error(f"Harvest API request failed: {e}")
            raise
