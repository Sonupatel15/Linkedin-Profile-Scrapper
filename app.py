# app.py
import streamlit as st
from datetime import datetime
from services.harvest_api import HarvestAPI
from services.profile_service import get_or_refresh_profile
from config.config import get_env

# Page config
st.set_page_config(page_title="LinkedIn Profile Scraper", layout="wide")

st.title("🔍 LinkedIn Profile Scraper")

# Sidebar for inputs
st.sidebar.header("Search Filters")
name = st.sidebar.text_input("Enter Name (required)")
current_company = st.sidebar.text_input("Current/Present Company (optional)")
past_company = st.sidebar.text_input("Previous Company (optional)")
school = st.sidebar.text_input("School (optional)")
location = st.sidebar.text_input("Location (optional)")

page = st.sidebar.number_input("Page Number", min_value=1, value=1)
max_show = st.sidebar.number_input("Max Profiles to Show", min_value=1, max_value=10, value=5)

default_fresh = int(get_env("FRESHNESS_DAYS", 30))
freshness_days = st.sidebar.selectbox("Freshness Days", options=[30, 60], index=0)

# Button to trigger search
if st.sidebar.button("Search Profiles"):

    if not name:
        st.error("Name is required to search profiles.")
    else:
        api = HarvestAPI()
        with st.spinner("Fetching profiles from Harvest API..."):
            try:
                result = api.search_profiles(
                    name=name,
                    current_company=current_company or None,
                    past_company=past_company or None,
                    school=school or None,
                    location=location or None,
                    page=page,
                )
                elements = result.get("elements", [])
                if not elements:
                    st.warning("No profiles found for this query.")
                else:
                    # Build list of LinkedIn URLs
                    links = []
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
                        st.warning("No valid LinkedIn profile links in results.")
                    else:
                        st.success(f"Found {len(links)} profiles")
                        # Display profiles as clickable buttons
                        selected_idx = st.radio(
                            "Select a profile to fetch details:", list(range(1, len(links) + 1)),
                            format_func=lambda x: links[x - 1]
                        )

                        selected_link = links[selected_idx - 1]

                        st.info("Fetching profile details from StaffSpy/DB...")
                        data = get_or_refresh_profile(selected_link, freshness_days=freshness_days)

                        if not data:
                            st.error("Could not fetch profile data.")
                        else:
                            st.success("✅ Profile Data Retrieved")
                            # Display preferred fields first
                            preferred = [
                                "linkedin_url","name","first_name","last_name","headline","location",
                                "company","past_company1","past_company2","school1","school2","last_updated"
                            ]
                            for k in preferred:
                                if k in data and data[k]:
                                    st.write(f"**{k.replace('_', ' ').title()}:** {data[k]}")

                            # Show remaining fields
                            for k, v in data.items():
                                if k not in preferred and v:
                                    st.write(f"**{k.replace('_', ' ').title()}:** {v}")

            except Exception as e:
                st.error(f"Error fetching profiles: {e}")
