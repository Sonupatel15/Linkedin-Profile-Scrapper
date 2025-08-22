import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import urllib.parse
from config.config import get_env

# === Logging Setup ===
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# === Load Database Credentials from Environment Variables ===
DB_USER = get_env("DB_USER", required=True)
DB_PASS_RAW = get_env("DB_PASS", required=True)  # Using get_env for consistency and logging
DB_PASS = urllib.parse.quote_plus(DB_PASS_RAW)   # URL-encode the password in case it has special characters
DB_HOST = get_env("DB_HOST", required=True)
DB_PORT = get_env("DB_PORT", required=True)
DB_NAME = get_env("DB_NAME", required=True)

# === Build the PostgreSQL Database URL ===
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# === Create SQLAlchemy Engine and Session Factory ===
engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# Log successful engine creation
logging.info("SQLAlchemy engine created successfully.")


def init_db():
    """
    Initialize the database by creating tables defined in the models.

    This function imports the Base metadata from the models module and creates
    all tables in the connected database if they don't already exist.
    """
    try:
        from database.models import Base  # Local import to avoid circular imports
        Base.metadata.create_all(bind=engine)
        logging.info("Database initialized and tables created successfully.")
    except Exception as e:
        logging.error(f"Error initializing database: {e}")
        raise
