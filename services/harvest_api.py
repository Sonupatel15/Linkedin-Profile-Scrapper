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
