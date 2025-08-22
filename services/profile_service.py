import os
import logging
from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError

from database.db import SessionLocal
from database.models import Profile
from services.staff_spy import StaffSpyService
from utils.helpers import extract_linkedin_id

# === Logging Setup ===
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
staffspy = StaffSpyService()


def _age_in_days(ts) -> int:
    """
    Calculate how many days ago the given timestamp was.
    Treats both naive and timezone-aware datetime objects.

    Args:
        ts (datetime): A datetime object (e.g., from DB)

    Returns:
        int: Number of days since the timestamp; very large number if None
    """
    if not ts:
        return 10**9  # Return a large number if no timestamp (means very old)

    now = datetime.now(tz=timezone.utc).replace(tzinfo=None)

    if hasattr(ts, "tzinfo") and ts.tzinfo is not None:
        ts = ts.astimezone(timezone.utc).replace(tzinfo=None)

    return (now - ts).days


def get_or_refresh_profile(linkedin_url: str, freshness_days: int = 30):
    """
    Retrieves a LinkedIn profile from the database if it's fresh.
    Otherwise, fetches from StaffSpy API and upserts into the database.

    Args:
        linkedin_url (str): The LinkedIn profile URL to fetch.
        freshness_days (int): Max age in days for data to be considered fresh.

    Returns:
        dict or None: The profile data as a dictionary, or None if not found/fetched.
    """
    db = SessionLocal()

    try:
        # Attempt to fetch profile from DB
        prof = db.query(Profile).filter(Profile.linkedin_url == linkedin_url).first()

        if prof and _age_in_days(prof.last_updated) <= freshness_days:
            logger.info(f"Using fresh profile from DB for: {linkedin_url}")
            return _to_dict(prof)

        # Fetch new data using StaffSpy
        linkedin_id = extract_linkedin_id(linkedin_url)
        newdata = staffspy.fetch_profile(linkedin_id)

        if not newdata:
            logger.warning(f"No data returned from StaffSpy for: {linkedin_url}")
            return _to_dict(prof) if prof else None

        # If profile doesn't exist in DB, create one
        if not prof:
            prof = Profile(linkedin_url=linkedin_url)

        # Update the profile with new data
        for field in [
            "name", "first_name", "last_name", "location", "headline",
            "company", "past_company1", "past_company2", "school1", "school2",
            "skills", "experiences", "certifications"
        ]:
            setattr(prof, field, newdata.get(field))

        # Commit changes to the database
        db.add(prof)
        db.commit()
        db.refresh(prof)

        logger.info(f"Profile for {linkedin_url} refreshed and saved to DB.")
        return _to_dict(prof)

    except SQLAlchemyError as e:
        logger.exception(f"Database error while processing {linkedin_url}: {e}")
        db.rollback()
        return None

    finally:
        db.close()


def _to_dict(prof: Profile):
    """
    Convert SQLAlchemy Profile object into a dictionary.

    Args:
        prof (Profile): SQLAlchemy profile object

    Returns:
        dict or None: Dictionary of profile fields or None
    """
    if not prof:
        return None

    return {column.name: getattr(prof, column.name) for column in prof.__table__.columns}
