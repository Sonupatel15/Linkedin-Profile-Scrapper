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


###############################################

# from services.harvest_api import HarvestAPI
# import json

# def main():
#     api = HarvestAPI()
#     name = input("Enter Name (required): ").strip()
#     if not name:
#         print("Name is required. Exiting.")
#         return

#     # Optional filters
#     current_company = input("Current Company (optional): ").strip() or None
#     past_company = input("Past Company (optional): ").strip() or None
#     school = input("School (optional): ").strip() or None
#     location = input("Location (optional): ").strip() or None
#     page = input("Page number (default 1): ").strip()
#     page = int(page) if page.isdigit() else 1

#     result = api.search_profiles(
#         name=name,
#         current_company=current_company,
#         past_company=past_company,
#         school=school,
#         location=location,
#         page=page
#     )

#     print("\n=== Result from HarvestAPI ===")
#     print(json.dumps(result, indent=2))

# if __name__ == "__main__":
#     main()


##################################

# from services.harvest_api import HarvestAPI

# def main():
#     api = HarvestAPI()
#     name = input("Enter Name (required): ").strip()
#     if not name:
#         print("Name is required. Exiting.")
#         return

#     # Optional filters
#     current_company = input("Current Company (optional): ").strip() or None
#     past_company = input("Past Company (optional): ").strip() or None
#     school = input("School (optional): ").strip() or None
#     location = input("Location (optional): ").strip() or None
#     page = input("Page number (default 1): ").strip()
#     page = int(page) if page.isdigit() else 1

#     result = api.search_profiles(
#         name=name,
#         current_company=current_company,
#         past_company=past_company,
#         school=school,
#         location=location,
#         page=page
#     )

#     # Extract and print profile links
#     elements = result.get("elements", [])
#     if not elements:
#         print("\n❌ No profiles found for this query.")
#         return

#     print("\n=== Matching Profile Links ===")
#     for i, profile in enumerate(elements, start=1):
#         # Some APIs return "url", others "linkedinUrl" or buildable from "publicIdentifier"
#         link = (
#             profile.get("url")
#             or profile.get("linkedinUrl")
#             or f"https://www.linkedin.com/in/{profile.get('publicIdentifier')}"
#         )
#         if link:
#             print(f"{i}. {link}")

# if __name__ == "__main__":
#     main()

######################################

# from services.harvest_api import HarvestAPI
# from services.profile_service import get_profile

# def main():
#     api = HarvestAPI()
#     name = input("Enter Name (required): ").strip()
#     if not name:
#         print("Name is required. Exiting.")
#         return

#     # Optional filters
#     current_company = input("Current Company (optional): ").strip() or None
#     past_company = input("Past Company (optional): ").strip() or None
#     school = input("School (optional): ").strip() or None
#     location = input("Location (optional): ").strip() or None
#     page = input("Page number (default 1): ").strip()
#     page = int(page) if page.isdigit() else 1

#     result = api.search_profiles(
#         name=name,
#         current_company=current_company,
#         past_company=past_company,
#         school=school,
#         location=location,
#         page=page
#     )

#     # Extract and print profile links
#     elements = result.get("elements", [])
#     if not elements:
#         print("\n❌ No profiles found for this query.")
#         return

#     print("\n=== Matching Profile Links ===")
#     links = []
#     for i, profile in enumerate(elements, start=1):
#         link = (
#             profile.get("url")
#             or profile.get("linkedinUrl")
#             or f"https://www.linkedin.com/in/{profile.get('publicIdentifier')}"
#         )
#         if link:
#             links.append(link)
#             print(f"{i}. {link}")

#     choice = input("\nEnter profile number to fetch details: ").strip()
#     if not choice.isdigit() or int(choice) < 1 or int(choice) > len(links):
#         print("❌ Invalid choice.")
#         return

#     selected_link = links[int(choice) - 1]
#     data = get_profile(selected_link)

#     if data:
#         print("\n✅ Profile Data:\n")
#         for k, v in data.items():
#             print(f"{k}: {v}")
#     else:
#         print("❌ Could not fetch profile data.")

# if __name__ == "__main__":
#     main()


###################

import logging
import os
from config.config import get_env
from database.db import init_db
from services.harvest_api import HarvestAPI
from services.profile_service import get_or_refresh_profile

# Basic logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger("").addHandler(console)

def ask_int(prompt, default=None, min_val=None, max_val=None):
    val = input(prompt).strip()
    if val == "" and default is not None:
        return default
    if not val.isdigit():
        return default
    num = int(val)
    if min_val is not None and num < min_val:
        num = min_val
    if max_val is not None and num > max_val:
        num = max_val
    return num

def main():
    # Ensure DB tables exist
    init_db()

    api = HarvestAPI()

    name = input("Enter Name (required): ").strip()
    if not name:
        print("Name is required. Exiting.")
        return

    current_company = input("Current/Present Company (optional): ").strip() or None
    past_company    = input("Previous Company (optional): ").strip() or None
    location        = input("Location (optional): ").strip() or None
    school          = input("School (optional): ").strip() or None

    page = ask_int("Page number (default 1): ", default=1, min_val=1)
    max_show = ask_int("How many profile links do you need? (max 10): ", default=5, min_val=1, max_val=10)

    # Freshness (30 or 60)
    default_fresh = int(get_env("FRESHNESS_DAYS", 30))
    freshness_days = ask_int(f"Freshness days (30/60, default {default_fresh}): ",
                             default=default_fresh, min_val=1, max_val=365)

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
        return

    # Build a list of LinkedIn URLs and show up to max_show
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
        return

    for idx, link in enumerate(links, start=1):
        print(f"{idx}. {link}")

    choice = input("\nEnter the profile number to fetch details: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(links)):
        print("❌ Invalid choice.")
        return

    selected_link = links[int(choice) - 1]
    data = get_or_refresh_profile(selected_link, freshness_days=freshness_days)

    if not data:
        print("❌ Could not fetch profile data.")
        return

    print("\n✅ Profile Data:\n")
    # Show a subset in nice order
    preferred = [
        "linkedin_url","name","first_name","last_name","headline","location",
        "company","past_company1","past_company2","school1","school2",
        "last_updated"
    ]
    for k in preferred:
        if k in data:
            print(f"{k}: {data[k]}")
    # show the rest
    for k, v in data.items():
        if k not in preferred:
            print(f"{k}: {v}")

if __name__ == "__main__":
    main()

###############################################
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


# def run_scraper(
#     name,
#     current_company=None,
#     past_company=None,
#     location=None,
#     school=None,
#     page=1,
#     max_show=5,
#     freshness_days=None,
# ):
#     """Reusable function for both CLI and Streamlit frontend."""
#     init_db()
#     api = HarvestAPI()

#     if not name:
#         raise ValueError("Name is required.")

#     if freshness_days is None:
#         freshness_days = int(get_env("FRESHNESS_DAYS", 30))

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
#         return {"profiles": [], "data": None}

#     # Collect links
#     links = []
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
#         return {"profiles": [], "data": None}

#     # Just return details of first profile (or could be extended for multiple)
#     selected_link = links[0]
#     data = get_or_refresh_profile(selected_link, freshness_days=freshness_days)

#     return {"profiles": links, "data": data}


# def main():
#     """CLI mode with inputs."""
#     name = input("Enter Name (required): ").strip()
#     if not name:
#         print("Name is required. Exiting.")
#         return

#     current_company = input("Current/Present Company (optional): ").strip() or None
#     past_company    = input("Previous Company (optional): ").strip() or None
#     location        = input("Location (optional): ").strip() or None
#     school          = input("School (optional): ").strip() or None

#     page = int(input("Page number (default 1): ") or 1)
#     max_show = int(input("How many profile links do you need? (max 10): ") or 5)

#     default_fresh = int(get_env("FRESHNESS_DAYS", 30))
#     freshness_days = int(input(f"Freshness days (default {default_fresh}): ") or default_fresh)

#     result = run_scraper(
#         name=name,
#         current_company=current_company,
#         past_company=past_company,
#         location=location,
#         school=school,
#         page=page,
#         max_show=max_show,
#         freshness_days=freshness_days,
#     )

#     if not result["profiles"]:
#         print("\n❌ No profiles found for this query.")
#         return

#     print("\n=== Matching Profile Links ===")
#     for idx, link in enumerate(result["profiles"], start=1):
#         print(f"{idx}. {link}")

#     if result["data"]:
#         print("\n✅ Profile Data:\n")
#         for k, v in result["data"].items():
#             print(f"{k}: {v}")


# if __name__ == "__main__":
#     main()
