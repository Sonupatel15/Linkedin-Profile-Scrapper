import os
import logging
from dotenv import load_dotenv

# === Logging Setup ===
# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging to write to logs/app.log with appropriate level and format
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load environment variables from a .env file into the system environment
load_dotenv()


def get_env(key: str, default=None, required: bool = False):
    """
    Retrieve an environment variable with optional default and required checks.

    Args:
        key (str): The name of the environment variable to retrieve.
        default (any, optional): The default value to return if the environment variable is not found. Defaults to None.
        required (bool, optional): Whether this environment variable is required. If True and the variable is missing or empty, raises a RuntimeError.

    Returns:
        str or any: The value of the environment variable, or the default value if not found and not required.

    Raises:
        RuntimeError: If the environment variable is required but missing or empty.
    """
    val = os.getenv(key, default)

    if required and (val is None or str(val).strip() == ""):
        logging.error(f"Missing required environment variable: {key}")
        raise RuntimeError(f"Missing required environment variable: {key}")

    logging.info(f"Environment variable '{key}' retrieved successfully.")
    return val
