# app.py
import streamlit as st
import pandas as pd
from main import run_scraper
from database.db import get_all_profiles

st.set_page_config(page_title="LinkedIn StaffSpy", layout="wide")
st.title("🔎 LinkedIn StaffSpy")
st.write("Search for employees of a company on LinkedIn and analyze the results.")

# Sidebar Inputs
st.sidebar.header("Search Settings")
name = st.sidebar.text_input("Name (required)", "Satya Nadella")
current_company = st.sidebar.text_input("Current Company")
past_company = st.sidebar.text_input("Past Company")
location = st.sidebar.text_input("Location")
school = st.sidebar.text_input("School")
page = st.sidebar.number_input("Page number", min_value=1, value=1)
max_show = st.sidebar.slider("How many profile links?", 1, 10, 5)
freshness_days = st.sidebar.selectbox("Freshness days", [30, 60], index=0)

if st.sidebar.button("Run Scraper"):
    with st.spinner("Scraping in progress..."):
        try:
            result = run_scraper(
                name=name,
                current_company=current_company or None,
                past_company=past_company or None,
                location=location or None,
                school=school or None,
                page=page,
                max_show=max_show,
                freshness_days=freshness_days,
            )
            if not result["profiles"]:
                st.error("❌ No profiles found.")
            else:
                st.success("✅ Scraping finished!")
                st.write("### Matching Profile Links")
                for idx, link in enumerate(result["profiles"], start=1):
                    st.write(f"{idx}. {link}")

                if result["data"]:
                    st.write("### Profile Data")
                    df = pd.DataFrame([result["data"]])
                    st.dataframe(df, use_container_width=True)

                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button("Download Profile CSV", csv, "profile.csv", "text/csv")
        except Exception as e:
            st.error(f"Error: {e}")

if st.button("Show All Saved Results from DB"):
    profiles = get_all_profiles()
    if profiles:
        df = pd.DataFrame([p.to_dict() for p in profiles])
        st.subheader("📊 Results from DB")
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download All CSV", csv, "profiles.csv", "text/csv")
    else:
        st.warning("No profiles found in the database.")
