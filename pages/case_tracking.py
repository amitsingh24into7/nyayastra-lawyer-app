# pages/case_tracking.py
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime

def show():
    st.subheader("🔍 Track Your Case")
    st.markdown("Search by case number or party name to get real-time updates from eCourts")

    # --- SEARCH INPUT ---
    search_type = st.radio("Search By", ["Case Number", "Party Name"],key="case_search_type")
    
    if search_type == "Case Number":
        case_number = st.text_input("Enter Case Number (e.g., CRIMINAL APPEAL No. 123 of 2020)")
        if st.button("🔍 Search Case", use_container_width=True):
            if case_number:
                with st.spinner("Fetching case details from eCourts..."):
                    case_data = search_case_by_number(case_number)
                    if case_data:
                        display_case_details(case_data)
                    else:
                        st.error("❌ No case found. Please check the case number.")
            else:
                st.warning("Please enter a case number")

    else:
        party_name = st.text_input("Enter Petitioner or Respondent Name")
        court_level = st.selectbox("Select Court Level", ["District Court", "High Court", "Supreme Court"], key="court_level_select")
        if st.button("🔍 Search by Name", use_container_width=True):
            if party_name:
                with st.spinner("Searching cases..."):
                    cases = search_cases_by_name(party_name, court_level)
                    if cases:
                        st.success(f"✅ Found {len(cases)} case(s)")
                        for case in cases:
                            with st.expander(f"**{case['case_no']}** | {case['act']}"):
                                for key, val in case.items():
                                    st.markdown(f"**{key.title().replace('_', ' ')}:** {val}")
                    else:
                        st.info("No cases found for this name.")
            else:
                st.warning("Please enter a name")

# --- SEARCH BY CASE NUMBER ---
def search_case_by_number(case_number):
    url = "https://njdg.ecourts.gov.in/njdgnew/index.php?mod=1&dt=25-08-2025&dt_to=25-08-2025"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://njdg.ecourts.gov.in/njdgnew/"
    }
    try:
        session = requests.Session()
        # Load main page to get cookies
        session.get("https://njdg.ecourts.gov.in/njdgnew/", headers=headers)

        # Simulate form submission
        response = session.post(url, data={
            "cino_search": case_number.strip(),
            "Submit": "Search"
        }, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find("table", {"class": "table table-striped table-bordered"})
        
        if not table:
            return None

        rows = table.find_all("tr")[1:]  # Skip header
        if not rows:
            return None

        first_row = rows[0]
        cols = first_row.find_all("td")
        data = [col.get_text(strip=True) for col in cols]

        return {
            "Case Number": data[0],
            "Court": data[1],
            "Act": data[2],
            "Petitioner": data[3],
            "Respondent": data[4],
            "Filing Date": data[5],
            "Next Date": data[6],
            "Status": data[7],
            "Judge": data[8] if len(data) > 8 else "Not Available"
        }
    except Exception as e:
        st.error(f"Error fetching case: {e}")
        return None

# --- SEARCH BY PARTY NAME ---
def search_cases_by_name(party_name, court_level):
    # This is simplified — in reality, you'd target specific court APIs
    # For demo, we'll return mock data
    return [
        {
            "case_no": "CRIMINAL APPEAL No. 123 of 2020",
            "court": "Delhi High Court",
            "act": "Indian Penal Code",
            "petitioner": party_name.title(),
            "respondent": "State of Delhi",
            "filing_date": "15-03-2020",
            "next_date": "30-08-2025",
            "status": "Listed",
            "judge": "Justice A.K. Gupta"
        }
    ]

# --- DISPLAY CASE DETAILS ---
def display_case_details(case_data):
    st.markdown("### 🏛️ Case Details")
    col1, col2, col3 = st.columns(3)
    col1.metric("Court", case_data["Court"])
    col2.metric("Next Date", case_data["Next Date"])
    col3.metric("Status", case_data["Status"])

    st.markdown("---")
    for key, value in case_data.items():
        st.markdown(f"**{key}:** {value}")

    # Timeline
    st.markdown("### 📅 Timeline")
    st.timeline([
        {
            "title": "Filed",
            "date": case_data["Filing Date"],
            "icon": "📁"
        },
        {
            "title": "Hearing",
            "date": case_data["Next Date"],
            "icon": "⚖️"
        },
        {
            "title": "Status",
            "content": case_data["Status"],
            "date": "Today",
            "icon": "📊"
        }
    ])

# --- RENDER PAGE ---
show()