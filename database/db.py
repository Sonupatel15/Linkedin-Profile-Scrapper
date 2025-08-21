from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import urllib
from config.config import get_env
import os

DB_USER = get_env("DB_USER", required=True)
DB_PASS = urllib.parse.quote_plus(os.getenv("DB_PASS"))
DB_HOST = get_env("DB_HOST", required=True)
DB_PORT = get_env("DB_PORT", required=True)
DB_NAME = get_env("DB_NAME", required=True)

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def init_db():
    """Create tables if they don't exist."""
    from database.models import Base  # local import to avoid circulars
    Base.metadata.create_all(bind=engine)
