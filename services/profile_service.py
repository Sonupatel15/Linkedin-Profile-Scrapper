import logging
from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError

from database.db import SessionLocal
from database.models import Profile
from services.staff_spy import StaffSpyService
from utils.helpers import extract_linkedin_id

logger = logging.getLogger(__name__)
staffspy = StaffSpyService()

def _age_in_days(ts) -> int:
    if not ts:
        return 10**9
    # Treat DB timestamp as naive/UTC-agnostic; compare to now()
    now = datetime.now(tz=timezone.utc).replace(tzinfo=None)
    if hasattr(ts, "tzinfo") and ts.tzinfo is not None:
        ts = ts.astimezone(timezone.utc).replace(tzinfo=None)
    return (now - ts).days

def get_or_refresh_profile(linkedin_url: str, freshness_days: int = 30):
    """
    1) Look up by linkedin_url
    2) If fresh -> return DB
    3) Else -> fetch via StaffSpy and UPSERT
    """
    db = SessionLocal()
    try:
        prof = db.query(Profile).filter(Profile.linkedin_url == linkedin_url).first()
        if prof and _age_in_days(prof.last_updated) <= freshness_days:
            return _to_dict(prof)

        # Fetch fresh data
        linkedin_id = extract_linkedin_id(linkedin_url)
        newdata = staffspy.fetch_profile(linkedin_id)
        if not newdata:
            # fallback to stale if exists
            return _to_dict(prof) if prof else None

        if not prof:
            prof = Profile(linkedin_url=linkedin_url)

        # Update fields
        for field in [
            "name","first_name","last_name","location","headline",
            "company","past_company1","past_company2","school1","school2",
            "skills","experiences","certifications"
        ]:
            setattr(prof, field, newdata.get(field))

        db.add(prof)
        db.commit()
        db.refresh(prof)
        return _to_dict(prof)

    except SQLAlchemyError as e:
        logger.exception(f"DB error: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def _to_dict(prof: Profile):
    if not prof:
        return None
    d = {c.name: getattr(prof, c.name) for c in prof.__table__.columns}
    return d


##########################################################################


# import json
# import logging
# from sqlalchemy.exc import SQLAlchemyError

# logger = logging.getLogger("StaffSpy")

# def _sanitize_string(value):
#     """Remove problematic characters from strings (like null bytes)."""
#     if value is None:
#         return None
#     return str(value).replace("\u0000", "").strip()

# def _sanitize_json_field(data):
#     """Convert data to JSON string and remove null bytes."""
#     if data is None:
#         return None
#     # If data is not a string, serialize to JSON
#     if isinstance(data, (dict, list)):
#         data_str = json.dumps(data, ensure_ascii=False)
#     else:
#         data_str = str(data)
#     # Remove null bytes
#     data_str = data_str.replace("\u0000", "")
#     return data_str

# def get_or_refresh_profile(db, newdata, freshness_days=30):
#     """
#     Save or update a LinkedIn profile in the database with proper sanitization.
#     """
#     try:
#         from models import Profile  # Adjust import based on your project structure

#         # Assume linkedin_url is unique
#         linkedin_url = newdata.get("linkedin_url")
#         prof = db.query(Profile).filter_by(linkedin_url=linkedin_url).first()
#         if not prof:
#             prof = Profile(linkedin_url=_sanitize_string(linkedin_url))
#             db.add(prof)

#         # Sanitize string fields
#         string_fields = [
#             "name", "first_name", "last_name", "location", "headline",
#             "company", "past_company1", "past_company2", "school1", "school2"
#         ]
#         for field in string_fields:
#             setattr(prof, field, _sanitize_string(newdata.get(field)))

#         # Sanitize JSON fields
#         json_fields = ["skills", "experiences", "certifications"]
#         for field in json_fields:
#             setattr(prof, field, _sanitize_json_field(newdata.get(field)))

#         db.commit()
#         logger.info(f"Profile saved/updated successfully: {linkedin_url}")
#         return prof

#     except SQLAlchemyError as e:
#         db.rollback()
#         logger.error(f"DB error while saving profile: {str(e)}")
#         return None

#     except Exception as e:
#         db.rollback()
#         logger.error(f"Unexpected error: {str(e)}")
#         return None
