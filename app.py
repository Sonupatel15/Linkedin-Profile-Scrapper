import streamlit as st
import pandas as pd
from services.harvest_api import HarvestAPI
from services.profile_service import get_or_refresh_profile
from services.bulk_service import fetch_profiles_from_urls
from config.config import get_env
from services.summarizer import summarize_profile
from utils.helpers import safe_parse_jsonish

st.set_page_config(page_title="LinkedIn Profile Scraper", layout="wide")
st.title("🔍 LinkedIn Profile Scraper")

# --- Helper Functions ---
def render_skills(skills_data):
    skills = safe_parse_jsonish(skills_data)
    if not skills:
        st.write("No skills data available.")
        return
    for skill in skills:
        skill_name = skill.get("name") if isinstance(skill, dict) else skill
        endorsements = skill.get("endorsements", 0) if isinstance(skill, dict) else 0
        passed = " ✅" if isinstance(skill, dict) and skill.get("passed_assessment") else ""
        st.write(f"- {skill_name} ({endorsements} endorsements){passed}")

def render_experiences(experiences_data):
    experiences = safe_parse_jsonish(experiences_data)
    if not experiences:
        st.write("No experiences data available.")
        return
    for exp in experiences:
        if not isinstance(exp, dict):
            st.write(exp)
            continue
        role = exp.get("title", "N/A")
        company = exp.get("company", "N/A")
        duration = exp.get("duration", "N/A")
        location = exp.get("location", "N/A")
        start = exp.get("start_date", "N/A")
        end = exp.get("end_date") or "Present"
        st.markdown(f"""
        **{role}** @ {company}  
        📅 {start} → {end}  ({duration})  
        🌍 {location}  
        """)
        st.markdown("---")

def render_certificates(certificates_data):
    certificates = safe_parse_jsonish(certificates_data)
    if not certificates:
        st.write("No certificates data available.")
        return
    for cert in certificates:
        if not isinstance(cert, dict):
            st.write(cert)
            continue
        title = cert.get("title", "N/A")
        issuer = cert.get("issuer", "N/A")
        date_issued = cert.get("date_issued", "N/A")
        cert_link = cert.get("cert_link")
        if cert_link:
            st.markdown(f"- **[{title}]({cert_link})** — *{issuer}* ({date_issued})")
        else:
            st.markdown(f"- **{title}** — *{issuer}* ({date_issued})")

def display_profile(data):
    if not data:
        st.error("Could not fetch profile data.")
        return

    preferred = [
        "linkedin_url", "name", "first_name", "last_name", "headline", "location",
        "company", "past_company1", "past_company2", "school1", "school2", "last_updated"
    ]
    for k in preferred:
        if k in data and data[k]:
            st.write(f"**{k.replace('_', ' ').title()}:** {data[k]}")

    if "skills" in data and data["skills"]:
        with st.expander("💡 Skills", expanded=True):
            render_skills(data["skills"])

    if "experiences" in data and data["experiences"]:
        with st.expander("📌 Work Experience", expanded=True):
            render_experiences(data["experiences"])

    if "certifications" in data and data["certifications"]:
        with st.expander("🎓 Certifications", expanded=True):
            render_certificates(data["certifications"])

    for k, v in data.items():
        if k not in preferred and v and k not in ["skills", "experiences", "certifications"]:
            st.write(f"**{k.replace('_', ' ').title()}:** {v}")

    st.subheader("📝 AI Summary of Profile")
    summary = summarize_profile(data)
    st.write(summary)

# --- Main App Views ---
def search_by_name():
    name = st.text_input("Enter Name (required)")
    current_company = st.text_input("Current/Present Company (optional)")
    past_company = st.text_input("Previous Company (optional)")
    school = st.text_input("School (optional)")
    location = st.text_input("Location (optional)")
    page = st.number_input("Page Number", min_value=1, value=1)
    max_show = st.number_input("Max Profiles to Show", min_value=1, max_value=10, value=5)
    freshness_days = st.selectbox("Freshness Days", options=[30, 60], index=0)

    if st.button("Search Profiles"):
        if not name:
            st.error("Name is required to search profiles.")
            return

        api = HarvestAPI()
        with st.spinner("Fetching profiles..."):
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
                    st.warning("No profiles found.")
                    return

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
                    st.warning("No valid LinkedIn URLs found.")
                    return

                selected_idx = st.radio("Select a profile to fetch details:", list(range(1, len(links) + 1)),
                                        format_func=lambda x: links[x - 1])
                selected_link = links[selected_idx - 1]
                profile_data = get_or_refresh_profile(selected_link, freshness_days)
                display_profile(profile_data)

            except Exception as e:
                st.error(f"Error: {e}")

def search_by_id():
    url = st.text_input("Enter LinkedIn Profile URL")
    freshness_days = st.selectbox("Freshness Days", options=[30, 60], index=0)

    if st.button("Fetch Profile"):
        if not url or not url.startswith("http"):
            st.error("Please provide a valid LinkedIn URL.")
        else:
            profile_data = get_or_refresh_profile(url, freshness_days)
            display_profile(profile_data)

def search_by_csv():
    uploaded_file = st.file_uploader("Upload CSV with 'url' column", type=["csv"])
    freshness_days = st.selectbox("Freshness Days for all profiles", options=[30, 60], index=0)

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if 'url' not in df.columns:
            st.error("CSV must have a 'url' column.")
            return

        st.success(f"{len(df)} URLs loaded.")

        if st.button("Fetch All Profiles"):
            with st.spinner("Fetching all profiles..."):
                results = fetch_profiles_from_urls(df['url'].tolist(), freshness_days)
                for i, result in enumerate(results):
                    st.markdown(f"## Profile {i+1}")
                    if result['error']:
                        st.error(f"Error: {result['error']}")
                    else:
                        display_profile(result['profile'])

# --- Main Navigation ---
option = st.radio("Choose search method", ["Search by Name", "Search by Id", "Search by CSV"])
st.markdown("---")

if option == "Search by Name":
    search_by_name()
elif option == "Search by Id":
    search_by_id()
elif option == "Search by CSV":
    search_by_csv()
