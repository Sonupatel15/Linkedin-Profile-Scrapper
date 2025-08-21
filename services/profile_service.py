# import datetime
# from database.db import SessionLocal
# from database.models import Profile
# from services.staff_spy import StaffSpyService
# from utils.helpers import extract_linkedin_id

# STAFFSPY = StaffSpyService()

# def get_profile(linkedin_url: str, freshness_days: int = 30):
#     """
#     Check DB first, if fresh return data.
#     Otherwise fetch via StaffSpy, update DB, return.
#     """
#     db = SessionLocal()
#     profile = db.query(Profile).filter_by(linkedin_url=linkedin_url).first()

#     # Check freshness
#     if profile:
#         age = (datetime.datetime.now() - profile.last_updated).days
#         if age <= freshness_days:
#             db.close()
#             return profile.__dict__

#     # Else fetch via StaffSpy
#     linkedin_id = extract_linkedin_id(linkedin_url)
#     new_data = STAFFSPY.fetch_profile(linkedin_id)
#     if not new_data:
#         db.close()
#         return None

#     # Upsert
#     if profile:
#         for key in ["name","first_name","last_name","location","headline",
#                     "company","past_company1","past_company2","school1","school2",
#                     "skills","experiences","certifications"]:
#             setattr(profile, key, new_data.get(key))
#     else:
#         profile = Profile(
#             linkedin_url=linkedin_url,
#             name=new_data.get("name"),
#             first_name=new_data.get("first_name"),
#             last_name=new_data.get("last_name"),
#             location=new_data.get("location"),
#             headline=new_data.get("headline"),
#             company=new_data.get("company"),
#             past_company1=new_data.get("past_company1"),
#             past_company2=new_data.get("past_company2"),
#             school1=new_data.get("school1"),
#             school2=new_data.get("school2"),
#             skills=new_data.get("skills"),
#             experiences=new_data.get("experiences"),
#             certifications=new_data.get("certifications")
#         )
#         db.add(profile)

#     db.commit()
#     db.refresh(profile)
#     db.close()
#     return profile.__dict__


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
