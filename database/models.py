from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()

class Profile(Base):
    __tablename__ = "profiles"

    profile_id   = Column(Integer, primary_key=True, index=True)
    linkedin_url = Column(Text, unique=True, nullable=False)

    # Common identity fields
    name       = Column(String(255))
    first_name = Column(String(255))
    last_name  = Column(String(255))
    location   = Column(String(255))
    headline   = Column(Text)

    # Work & education summary
    company        = Column(String(255))    # current company
    past_company1  = Column(String(255))
    past_company2  = Column(String(255))
    school1        = Column(String(255))
    school2        = Column(String(255))

    # Rich fields
    skills         = Column(JSONB)          # e.g. [{"name": "...", "endorsements": 3}, ...] or ["A","B",...]
    experiences    = Column(JSONB)          # list of dicts
    certifications = Column(JSONB)          # list of dicts

    # Freshness
    last_updated = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
