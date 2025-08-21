# import os
# from dotenv import load_dotenv

# load_dotenv()

# def get_env_variables(key: str, default=None):
#     """Helper to fetch environment variables safely"""
#     return os.getenv(key, default)

# # Direct access if needed
# HARVEST_API_KEY = os.getenv("HARVEST_API_KEY")

####################
import os
from dotenv import load_dotenv

# Load .env once on import
load_dotenv()

def get_env(key: str, default=None, required: bool = False):
    val = os.getenv(key, default)
    if required and (val is None or str(val).strip() == ""):
        raise RuntimeError(f"Missing required env var: {key}")
    return val
