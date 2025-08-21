import os
from dotenv import load_dotenv

# Load .env once on import
load_dotenv()

def get_env(key: str, default=None, required: bool = False):
    val = os.getenv(key, default)
    if required and (val is None or str(val).strip() == ""):
        raise RuntimeError(f"Missing required env var: {key}")
    return val
