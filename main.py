# import logging
# import os
# from config.config import get_env
# from database.db import init_db
# from services.harvest_api import HarvestAPI
# from services.profile_service import get_or_refresh_profile

# # Basic logging
# os.makedirs("logs", exist_ok=True)
# logging.basicConfig(
#     filename="logs/app.log",
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )
# console = logging.StreamHandler()
# console.setLevel(logging.INFO)
# logging.getLogger("").addHandler(console)

# def ask_int(prompt, default=None, min_val=None, max_val=None):
#     val = input(prompt).strip()
#     if val == "" and default is not None:
#         return default
#     if not val.isdigit():
#         return default
#     num = int(val)
#     if min_val is not None and num < min_val:
#         num = min_val
#     if max_val is not None and num > max_val:
#         num = max_val
#     return num

# def main():
#     # Ensure DB tables exist
#     init_db()

#     api = HarvestAPI()

#     name = input("Enter Name (required): ").strip()
#     if not name:
#         print("Name is required. Exiting.")
#         return

#     current_company = input("Current/Present Company (optional): ").strip() or None
#     past_company    = input("Previous Company (optional): ").strip() or None
#     location        = input("Location (optional): ").strip() or None
#     school          = input("School (optional): ").strip() or None

#     page = ask_int("Page number (default 1): ", default=1, min_val=1)
#     max_show = ask_int("How many profile links do you need? (max 10): ", default=5, min_val=1, max_val=10)

#     # Freshness (30 or 60)
#     default_fresh = int(get_env("FRESHNESS_DAYS", 30))
#     freshness_days = ask_int(f"Freshness days (30/60, default {default_fresh}): ",
#                              default=default_fresh, min_val=1, max_val=365)

#     result = api.search_profiles(
#         name=name,
#         current_company=current_company,
#         past_company=past_company,
#         school=school,
#         location=location,
#         page=page,
#     )

#     elements = result.get("elements", [])
#     if not elements:
#         print("\n❌ No profiles found for this query.")
#         return

#     # Build a list of LinkedIn URLs and show up to max_show
#     links = []
#     print("\n=== Matching Profile Links ===")
#     for profile in elements:
#         link = (
#             profile.get("url")
#             or profile.get("linkedinUrl")
#             or (f"https://www.linkedin.com/in/{profile.get('publicIdentifier')}"
#                 if profile.get("publicIdentifier") else None)
#         )
#         if link:
#             links.append(link)
#         if len(links) >= max_show:
#             break

#     if not links:
#         print("\n❌ No valid LinkedIn profile links in results.")
#         return

#     for idx, link in enumerate(links, start=1):
#         print(f"{idx}. {link}")

#     choice = input("\nEnter the profile number to fetch details: ").strip()
#     if not choice.isdigit() or not (1 <= int(choice) <= len(links)):
#         print("❌ Invalid choice.")
#         return

#     selected_link = links[int(choice) - 1]
#     data = get_or_refresh_profile(selected_link, freshness_days=freshness_days)

#     if not data:
#         print("❌ Could not fetch profile data.")
#         return

#     print("\n✅ Profile Data:\n")
#     # Show a subset in nice order
#     preferred = [
#         "linkedin_url","name","first_name","last_name","headline","location",
#         "company","past_company1","past_company2","school1","school2",
#         "last_updated"
#     ]
#     for k in preferred:
#         if k in data:
#             print(f"{k}: {data[k]}")
#     # show the rest
#     for k, v in data.items():
#         if k not in preferred:
#             print(f"{k}: {v}")

# if __name__ == "__main__":
#     main()


import logging
import os
from config.config import get_env
from database.db import init_db
from services.harvest_api import HarvestAPI
from services.profile_service import get_or_refresh_profile

# === Setup logging to file and console ===
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger("").addHandler(console)

logger = logging.getLogger(__name__)


def ask_int(prompt, default=None, min_val=None, max_val=None):
    """
    Prompt user for an integer input, with optional default and bounds.

    Returns:
        int or None: Validated integer or default value if input is empty or invalid.
    """
    while True:
        val = input(prompt).strip()
        if val == "" and default is not None:
            return default
        if not val.isdigit():
            print("Please enter a valid number.")
            continue
        num = int(val)
        if min_val is not None and num < min_val:
            print(f"Number must be at least {min_val}.")
            continue
        if max_val is not None and num > max_val:
            print(f"Number must be at most {max_val}.")
            continue
        return num


def main():
    """
    Main program loop.

    - Initializes database tables.
    - Accepts user inputs for LinkedIn profile search.
    - Queries HarvestAPI for profiles.
    - Displays results and allows user to select a profile.
    - Fetches and displays detailed profile data.
    """
    logger.info("Application started")
    try:
        # Initialize DB tables if not exist
        init_db()
        logger.info("Database initialized")

        api = HarvestAPI()

        # Required name input
        name = input("Enter Name (required): ").strip()
        if not name:
            print("Name is required. Exiting.")
            logger.warning("User exited: no name entered.")
            return

        # Optional filters
        current_company = input("Current/Present Company (optional): ").strip() or None
        past_company = input("Previous Company (optional): ").strip() or None
        location = input("Location (optional): ").strip() or None
        school = input("School (optional): ").strip() or None

        # Pagination and result count
        page = ask_int("Page number (default 1): ", default=1, min_val=1)
        max_show = ask_int("How many profile links do you need? (max 10): ", default=5, min_val=1, max_val=10)

        # Freshness setting with fallback
        default_fresh = int(get_env("FRESHNESS_DAYS", 30))
        freshness_days = ask_int(
            f"Freshness days (30/60, default {default_fresh}): ",
            default=default_fresh, min_val=1, max_val=365
        )

        logger.info(f"Searching profiles with name='{name}', page={page}")

        # Query Harvest API
        result = api.search_profiles(
            name=name,
            current_company=current_company,
            past_company=past_company,
            school=school,
            location=location,
            page=page,
        )

        elements = result.get("elements", [])
        if not elements:
            print("\n❌ No profiles found for this query.")
            logger.info("No profiles found.")
            return

        # Extract LinkedIn profile links up to max_show
        links = []
        print("\n=== Matching Profile Links ===")
        for profile in elements:
            link = (
                profile.get("url")
                or profile.get("linkedinUrl")
                or (f"https://www.linkedin.com/in/{profile.get('publicIdentifier')}"
                    if profile.get("publicIdentifier") else None)
            )
            if link:
                links.append(link)
            if len(links) >= max_show:
                break

        if not links:
            print("\n❌ No valid LinkedIn profile links in results.")
            logger.info("No valid LinkedIn URLs found.")
            return

        # Display links to user
        for idx, link in enumerate(links, start=1):
            print(f"{idx}. {link}")

        # User selects which profile to fetch details for
        choice = input("\nEnter the profile number to fetch details: ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(links)):
            print("❌ Invalid choice.")
            logger.warning(f"Invalid profile selection: {choice}")
            return

        selected_link = links[int(choice) - 1]
        logger.info(f"Fetching profile data for {selected_link}")

        # Fetch profile from DB or StaffSpy service (with freshness)
        data = get_or_refresh_profile(selected_link, freshness_days=freshness_days)

        if not data:
            print("❌ Could not fetch profile data.")
            logger.error(f"Failed to fetch profile data for {selected_link}")
            return

        print("\n✅ Profile Data:\n")

        # Display preferred fields first, then any remaining fields
        preferred = [
            "linkedin_url", "name", "first_name", "last_name", "headline", "location",
            "company", "past_company1", "past_company2", "school1", "school2",
            "last_updated"
        ]
        for k in preferred:
            if k in data:
                print(f"{k}: {data[k]}")
        for k, v in data.items():
            if k not in preferred:
                print(f"{k}: {v}")

        logger.info("Profile data displayed successfully.")

    except Exception as e:
        logger.exception(f"Unexpected error in main: {e}")
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
