# import httpx
# import logging
# from config.config import get_env_variables

# # Configure logging
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(levelname)s - %(message)s')

# class HarvestAPI:
#     def __init__(self):
#         self.api_key = get_env_variables("HARVEST_API_KEY")
#         if not self.api_key:
#             logging.error("Harvest API Key not found in environment variables.")
#             raise ValueError("HARVEST_API_KEY must be set.")
#         self.base_url = "https://api.harvest-api.com"
#         self.client = httpx.Client(
#             base_url=self.base_url,
#             headers={"X-API-Key": self.api_key},
#             timeout=60.0
#         )

#     def search_profiles(self,
#                         name: str,
#                         current_company: str = None,
#                         past_company: str = None,
#                         school: str = None,
#                         location: str = None,
#                         page: int = 1):
#         """Search LinkedIn profiles using HarvestAPI."""
#         endpoint = "/linkedin/profile-search"
#         params = {"search": name, "page": str(page)}

#         if current_company:
#             params["currentCompany"] = current_company
#         if past_company:
#             params["pastCompany"] = past_company
#         if school:
#             params["school"] = school
#         if location:
#             params["location"] = location

#         try:
#             logging.info(f"Requesting HarvestAPI with params: {params}")
#             resp = self.client.get(endpoint, params=params)
#             resp.raise_for_status()
#             logging.info(f"Search successful, status code: {resp.status_code}")
#             return resp.json()
#         except httpx.HTTPStatusError as e:
#             logging.error(f"HTTP Error {e.response.status_code}: {e.response.text}")
#             return {"error": f"HTTP {e.response.status_code}", "details": e.response.text}
#         except httpx.RequestError as e:
#             logging.error(f"Request Error: {e}")
#             return {"error": "Request Error", "details": str(e)}
#         except Exception as e:
#             logging.error(f"Unexpected Error: {e}")
#             return {"error": "Unexpected Error", "details": str(e)}

#     def search_geo_id(self, location_query: str):
#         """Optional helper: Obtain LinkedIn GeoID for accurate location filtering."""
#         endpoint = "/linkedin/geo-id-search"
#         params = {"search": location_query}
#         try:
#             logging.info(f"Fetching GeoID for location: {location_query}")
#             resp = self.client.get(endpoint, params=params)
#             resp.raise_for_status()
#             return resp.json()
#         except Exception as e:
#             logging.error(f"Error fetching geo ID: {e}")
#             return {"error": "GeoID retrieval failed", "details": str(e)}

######################################

import logging
import requests
from config.config import get_env

logger = logging.getLogger(__name__)

class HarvestAPI:
    BASE_URL = "https://api.harvest-api.com/linkedin/profile-search"

    def __init__(self):
        self.api_key = get_env("HARVEST_API_KEY", required=True)

    def search_profiles(self, name, current_company=None, past_company=None,
                        school=None, location=None, page=1, limit=10):
        """
        Calls Harvest search and returns JSON.
        limit affects only how many we display (API may not support it directly).
        """
        params = {"search": name, "page": page}
        # If Harvest supports these filters, pass them through; if not, harmless.
        if current_company: params["currentCompany"] = current_company
        if past_company:    params["pastCompany"]    = past_company
        if school:          params["school"]         = school
        if location:        params["location"]       = location

        headers = {
            "x-api-key": self.api_key,
            "Authorization": f"Bearer {self.api_key}",  # support either style
            "Accept": "application/json",
        }

        logger.info(f"Requesting HarvestAPI with params: {params}")
        resp = requests.get(self.BASE_URL, params=params, headers=headers, timeout=30)
        logger.info(f"Search status code: {resp.status_code}")
        resp.raise_for_status()
        data = resp.json() if resp.content else {}
        # We don't trim to 'limit' here, we let main trim the displayed list.
        return data
