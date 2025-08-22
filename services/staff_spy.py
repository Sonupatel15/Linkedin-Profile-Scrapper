# import logging
# import pandas as pd
# from config.config import get_env
# from utils.helpers import safe_parse_jsonish, coalesce
# from staffspy import LinkedInAccount

# logger = logging.getLogger(__name__)

# class StaffSpyService:
#     def __init__(self):
#         session_file = get_env("STAFFSPY_SESSION_FILE", "session.pkl")
#         # log_level: 0 errors, 1 info, 2 debug (per their readme)
#         self.account = LinkedInAccount(session_file=session_file, log_level=1)

#     def fetch_profile(self, linkedin_id: str):
#         """
#         Returns a normalized dict compatible with our DB schema, or None.
#         """
#         try:
#             df: pd.DataFrame = self.account.scrape_users(user_ids=[linkedin_id])
#             if df is None or df.empty:
#                 return None
#             row = df.iloc[0].to_dict()

#             # Map StaffSpy fields (handles multiple possible column names)
#             name       = row.get("name")
#             first_name = row.get("first_name")
#             last_name  = row.get("last_name")
#             location   = row.get("location")
#             headline   = coalesce(row.get("headline"), row.get("position"), row.get("current_position"))

#             company       = coalesce(row.get("company"), row.get("current_company"))
#             past_company1 = coalesce(row.get("past_company1"), row.get("past_company_1"))
#             past_company2 = coalesce(row.get("past_company2"), row.get("past_company_2"))

#             school1 = coalesce(row.get("school1"), row.get("school_1"))
#             school2 = coalesce(row.get("school2"), row.get("school_2"))

#             # Skills may appear as a JSONish list OR split into top_skill_*
#             skills = safe_parse_jsonish(row.get("skills"))
#             if not skills:
#                 tops = [row.get("top_skill_1"), row.get("top_skill_2"), row.get("top_skill_3")]
#                 tops = [s for s in tops if s and str(s).strip()]
#                 if tops:
#                     skills = tops  # fallback simple list

#             experiences    = safe_parse_jsonish(row.get("experiences"))
#             certifications = safe_parse_jsonish(row.get("certifications"))

#             return {
#                 "name": name,
#                 "first_name": first_name,
#                 "last_name": last_name,
#                 "location": location,
#                 "headline": headline,
#                 "company": company,
#                 "past_company1": past_company1,
#                 "past_company2": past_company2,
#                 "school1": school1,
#                 "school2": school2,
#                 "skills": skills,
#                 "experiences": experiences,
#                 "certifications": certifications,
#             }
#         except Exception as e:
#             logger.exception(f"StaffSpy fetch failed for {linkedin_id}: {e}")
#             return None


import os
import logging
import pandas as pd
from config.config import get_env
from utils.helpers import safe_parse_jsonish, coalesce
from staffspy import LinkedInAccount

# === Logging Setup ===
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class StaffSpyService:
    """
    Wrapper class around the StaffSpy LinkedIn scraper.
    
    Loads a session file and fetches profile data using a LinkedIn ID.
    """

    def __init__(self):
        # Load the session file path from environment variable or default
        session_file = get_env("STAFFSPY_SESSION_FILE", "session.pkl")

        # Initialize the LinkedInAccount object with session and log level
        self.account = LinkedInAccount(session_file=session_file, log_level=1)

    def fetch_profile(self, linkedin_id: str):
        """
        Fetch a LinkedIn profile by ID and normalize it to match our DB schema.

        Args:
            linkedin_id (str): LinkedIn user ID (extracted from the profile URL)

        Returns:
            dict or None: A normalized dictionary of profile data, or None on failure
        """
        try:
            df: pd.DataFrame = self.account.scrape_users(user_ids=[linkedin_id])

            if df is None or df.empty:
                logger.warning(f"No data returned for LinkedIn ID: {linkedin_id}")
                return None

            row = df.iloc[0].to_dict()

            # Extract and normalize fields using fallback options where necessary
            name = row.get("name")
            first_name = row.get("first_name")
            last_name = row.get("last_name")
            location = row.get("location")
            headline = coalesce(row.get("headline"), row.get("position"), row.get("current_position"))

            company = coalesce(row.get("company"), row.get("current_company"))
            past_company1 = coalesce(row.get("past_company1"), row.get("past_company_1"))
            past_company2 = coalesce(row.get("past_company2"), row.get("past_company_2"))

            school1 = coalesce(row.get("school1"), row.get("school_1"))
            school2 = coalesce(row.get("school2"), row.get("school_2"))

            # Handle skills field which could be JSONish or broken up
            skills = safe_parse_jsonish(row.get("skills"))
            if not skills:
                tops = [
                    row.get("top_skill_1"),
                    row.get("top_skill_2"),
                    row.get("top_skill_3")
                ]
                tops = [s for s in tops if s and str(s).strip()]
                if tops:
                    skills = tops  # fallback to simple list if present

            experiences = safe_parse_jsonish(row.get("experiences"))
            certifications = safe_parse_jsonish(row.get("certifications"))

            logger.info(f"Successfully fetched profile for LinkedIn ID: {linkedin_id}")

            return {
                "name": name,
                "first_name": first_name,
                "last_name": last_name,
                "location": location,
                "headline": headline,
                "company": company,
                "past_company1": past_company1,
                "past_company2": past_company2,
                "school1": school1,
                "school2": school2,
                "skills": skills,
                "experiences": experiences,
                "certifications": certifications,
            }

        except Exception as e:
            logger.exception(f"StaffSpy fetch failed for LinkedIn ID {linkedin_id}: {e}")
            return None
