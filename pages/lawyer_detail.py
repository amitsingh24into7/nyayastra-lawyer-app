# pages/lawyer_detail.py
import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

# --- HIDE DEFAULT NAV ---
st.markdown(
    """
    <style>
    div[data-testid="stSidebarNav"] { display: none !important; }
    .stMarkdown, .stText { font-family: 'Inter', sans-serif; }
    </style>
    """,
    unsafe_allow_html=True
)

def show():
    # --- BACK BUTTON (SAFE) ---
    st.link_button("← Back to Lawyers", "pages/lawyers.py", use_container_width=True)
    st.divider()

    # --- CHECK FOR LAWYER ID ---
    if "lawyer_id" not in st.session_state:
        st.error("❌ No lawyer selected")
        st.link_button("Browse All Lawyers", "pages/lawyers.py", use_container_width=True)
        st.stop()

    lawyer_id = st.session_state.lawyer_id

    try:
        response = supabase.table("lawyers").select("*").eq("id", lawyer_id).execute()
        if not response:
            st.error("❌ Lawyer not found")
            st.link_button("← Back to Lawyers", "pages/lawyers.py", use_container_width=True)
            return
        lawyer = response.data[0]

        # --- HEADER ---
        col1, col2 = st.columns([1, 2])
        with col1:
            if lawyer["profile_image_url"]:
                st.image(lawyer["profile_image_url"], width=120)
            else:
                name_parts = lawyer["name"].split()
                initials = (name_parts[0][0] + name_parts[-1][0]).upper() if len(name_parts) > 1 else name_parts[0][0].upper()
                gender = lawyer.get("gender", "other")
                bg_color = "2563EB" if gender == "male" else "ee44ac" if gender == "female" else "059669"
                # ✅ Fix: bg_color is now a real string
                img_url = f"https://ui-avatars.com/api/?name={initials}&background={bg_color}&color=fff&size=128"
                st.image(img_url, width=120)

        with col2:
            st.markdown(f"<h2 style='color: #1E293B; margin: 0;'>{lawyer['name']}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #2563EB; font-weight: 600; margin: 0;'>{', '.join(lawyer['specialization'][:2])}</p>", unsafe_allow_html=True)
            st.markdown(f"📍 {lawyer['location']} | ⭐ {lawyer['rating']} | {lawyer['experience_years']} years")

        st.divider()

        # --- ABOUT ---
        st.markdown("### 📝 About")
        st.write(lawyer["about"])

        st.markdown("### 🎓 Education")
        st.write(lawyer["education"])

        st.markdown("### 🛠️ Practice Areas")
        practice_areas = lawyer.get("practice_areas") or lawyer["specialization"]
        st.markdown(" | ".join([f"`{area}`" for area in practice_areas[:5]]))

        st.markdown("### 🗣️ Languages Spoken")
        st.markdown(", ".join([f"**{lang}**" for lang in lawyer["languages"]]))

        st.divider()

        # --- PAST CASES ---
        st.markdown("### 🏛️ Notable Cases")
        cases = supabase.table("lawyer_cases").select("*").eq("lawyer_id", lawyer_id).execute().data
        if not cases:
            st.info("No case history available.")
        else:
            for case in cases:
                with st.expander(f"**{case['case_title']}** | {case['court']} ({case['year']})"):
                    st.markdown(f"**Type:** {case['case_type']} | **Outcome:** {case['outcome']}")
                    st.write(case['description'])
                    if case['client_feedback']:
                        st.markdown(f"> *Client: {case['client_feedback']}*")

        st.divider()

        # --- ACTION BUTTONS ---
        st.markdown("### 💬 Take Action")
        colA, colB, colC = st.columns(3)
        with colA:
            if st.button("📞 Call Lawyer", use_container_width=True):
                st.success(f"Calling {lawyer['phone']}...")

        with colB:
            wa_link = f"https://wa.me/{lawyer['phone'].replace('+', '')}?text=Hi+Advocate,+I+found+you+on+Nyastra+Pulse.+I+need+legal+help."
            st.markdown(
                f"<a href='{wa_link}' target='_blank' style='display: block; text-align: center; background: #10B981; color: white; padding: 0.5rem; border-radius: 8px; text-decoration: none;'>💬 WhatsApp</a>",
                unsafe_allow_html=True
            )

        with colC:
            if st.button("📅 Book ₹99 Consult", use_container_width=True):
                st.success("✅ Booking confirmed!")

    except Exception as e:
        st.error(f"❌ Failed to load profile: {str(e)}")

# Render page
show()