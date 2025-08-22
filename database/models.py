import logging
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import JSONB

# === Logging Setup ===
import os
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# === Base class for SQLAlchemy models ===
Base = declarative_base()


class Profile(Base):
    """
    SQLAlchemy model for the 'profiles' table.

    Represents a user profile, such as one pulled from LinkedIn or similar services.
    Stores identity, professional summary, education, and structured profile data.
    """

    __tablename__ = "profiles"

    # Primary key
    profile_id = Column(Integer, primary_key=True, index=True)

    # Required LinkedIn URL (must be unique)
    linkedin_url = Column(Text, unique=True, nullable=False)

    # Identity fields
    name = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    location = Column(String(255))
    headline = Column(Text)

    # Work and education
    company = Column(String(255))         # Current company
    past_company1 = Column(String(255))   # Past company 1
    past_company2 = Column(String(255))   # Past company 2
    school1 = Column(String(255))         # School 1
    school2 = Column(String(255))         # School 2

    # Rich structured fields (stored as JSONB)
    skills = Column(JSONB)                # e.g., [{"name": "Python", "endorsements": 3}]
    experiences = Column(JSONB)           # e.g., list of experience objects
    certifications = Column(JSONB)        # e.g., list of certification objects

    # Timestamp of last update (auto-updated on row change)
    last_updated = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
