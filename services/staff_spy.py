import logging
import pandas as pd
from config.config import get_env
from utils.helpers import safe_parse_jsonish, coalesce
from staffspy import LinkedInAccount

logger = logging.getLogger(__name__)

class StaffSpyService:
    def __init__(self):
        session_file = get_env("STAFFSPY_SESSION_FILE", "session.pkl")
        # log_level: 0 errors, 1 info, 2 debug (per their readme)
        self.account = LinkedInAccount(session_file=session_file, log_level=1)

    def fetch_profile(self, linkedin_id: str):
        """
        Returns a normalized dict compatible with our DB schema, or None.
        """
        try:
            df: pd.DataFrame = self.account.scrape_users(user_ids=[linkedin_id])
            if df is None or df.empty:
                return None
            row = df.iloc[0].to_dict()

            # Map StaffSpy fields (handles multiple possible column names)
            name       = row.get("name")
            first_name = row.get("first_name")
            last_name  = row.get("last_name")
            location   = row.get("location")
            headline   = coalesce(row.get("headline"), row.get("position"), row.get("current_position"))

            company       = coalesce(row.get("company"), row.get("current_company"))
            past_company1 = coalesce(row.get("past_company1"), row.get("past_company_1"))
            past_company2 = coalesce(row.get("past_company2"), row.get("past_company_2"))

            school1 = coalesce(row.get("school1"), row.get("school_1"))
            school2 = coalesce(row.get("school2"), row.get("school_2"))

            # Skills may appear as a JSONish list OR split into top_skill_*
            skills = safe_parse_jsonish(row.get("skills"))
            if not skills:
                tops = [row.get("top_skill_1"), row.get("top_skill_2"), row.get("top_skill_3")]
                tops = [s for s in tops if s and str(s).strip()]
                if tops:
                    skills = tops  # fallback simple list

            experiences    = safe_parse_jsonish(row.get("experiences"))
            certifications = safe_parse_jsonish(row.get("certifications"))

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
            logger.exception(f"StaffSpy fetch failed for {linkedin_id}: {e}")
            return None
