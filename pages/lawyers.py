# pages/lawyers.py
import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

def show():
    st.subheader("📞 Find a Verified Lawyer")
    st.markdown("Search by location, specialization, and experience")

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        location = st.text_input("📍 Location (City)")
    with col2:
        spec = st.selectbox(
            "🎯 Specialization",
            ["All", "Criminal", "Cheque Bounce", "Family Law", "Property", "Divorce", "Labour Law", "Cyber Law"]
        )

    # Build Query
    query = supabase.table("lawyers").select("*", count="exact")
    if location:
        query = query.ilike("location", f"%{location}%")
    if spec != "All":
        query = query.contains("specialization", [spec])

    try:
        response = query.execute()
        lawyers = response.data
        total = response.count
    except Exception as e:
        st.error(f"❌ Failed to load lawyers: {str(e)}")
        return

    if not lawyers:
        st.warning("No lawyers found for your search.")
        return

    # --- PAGINATION ---
    PAGE_SIZE = 5
    total_pages = (total // PAGE_SIZE) + (1 if total % PAGE_SIZE > 0 else 0)

    # Current page
    if "lawyers_page" not in st.session_state:
        st.session_state.lawyers_page = 1

    current_page = st.session_state.lawyers_page
    start_idx = (current_page - 1) * PAGE_SIZE
    end_idx = start_idx + PAGE_SIZE
    lawyers_to_show = lawyers[start_idx:end_idx]  # ✅ Define BEFORE sorting

    # --- SORTING ---
    sort_by = st.selectbox("Sort By", ["Relevance", "Highest Rated", "Lowest Fee"], key="sort_select")

    if sort_by == "Highest Rated":
        lawyers_to_show = sorted(lawyers_to_show, key=lambda x: x["rating"], reverse=True)
    elif sort_by == "Lowest Fee":
        lawyers_to_show = sorted(lawyers_to_show, key=lambda x: x["consultation_fee"])

    # --- DISPLAY LAWYERS ---
    for lawyer in lawyers_to_show:
        with st.container():
            # Recalculate initials and bg_color for each lawyer
            name_parts = lawyer["name"].split()
            initials = (name_parts[0][0] + name_parts[-1][0]).upper() if len(name_parts) > 1 else name_parts[0][0].upper()
            gender = lawyer.get("gender", "other")
            bg_color = "2563EB" if gender == "male" else "ee44ac" if gender == "female" else "059669"

            colA, colB, colC = st.columns([1, 3, 1])
            with colA:
                if lawyer["profile_image_url"]:
                    st.image(lawyer["profile_image_url"], width=80)
                else:
                    img_url = f"https://ui-avatars.com/api/?name={initials}&background={bg_color}&color=fff&size=128"
                    st.image(img_url, width=80)

            with colB:
                st.markdown(f"### {lawyer['name']}")
                specs = ", ".join(lawyer['specialization'][:2])
                st.markdown(f"**{specs}** | {lawyer['location']} | ⭐ {lawyer['rating']}")
                st.markdown(f"Experience: {lawyer['experience_years']} years | Fee: ₹{lawyer['consultation_fee']}")

            with colC:
                if st.button("📞", key=f"call_{lawyer['id']}"):
                    st.success(f"📞 Calling {lawyer['phone']}...")

            # WhatsApp Button (clean URL)
            wa_link = f"https://wa.me/{lawyer['phone'].replace('+', '')}?text=Hi+Advocate,+I+found+you+on+Nyastra+Pulse.+I+need+legal+help."
            st.markdown(
                f"<a href='{wa_link}' target='_blank' style='display: inline-block; background: #10B981; color: white; padding: 0.375rem 0.75rem; border-radius: 6px; text-decoration: none; font-size: 0.9rem; margin-left: 0.5rem;'>💬 WhatsApp</a>",
                unsafe_allow_html=True
            )

            # --- EXPANDER: Lawyer Details ---
            with st.expander("👁️ View Full Profile"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    if lawyer["profile_image_url"]:
                        st.image(lawyer["profile_image_url"], width=120)
                    else:
                        st.image(f"https://ui-avatars.com/api/?name={initials}&background={bg_color}&color=fff&size=128", width=120)

                with col2:
                    st.markdown(f"## {lawyer['name']}")
                    st.markdown(f"**{', '.join(lawyer['specialization'])}** | {lawyer['location']}")
                    st.markdown(f"📞 {lawyer['phone']} | ⭐ {lawyer['rating']} | {lawyer['experience_years']} years")

                st.divider()

                st.markdown("### 📝 About")
                st.write(lawyer["about"])

                st.markdown("### 🎓 Education")
                st.write(lawyer["education"])

                st.markdown("### 🛠️ Practice Areas")
                practice_areas = lawyer.get("practice_areas") or lawyer["specialization"]
                st.markdown(" | ".join([f"`{area}`" for area in practice_areas[:5]]))

                st.markdown("### 🗣️ Languages Spoken")
                st.markdown(", ".join([f"**{lang}**" for lang in lawyer["languages"]]))

                st.markdown("### 🏛️ Notable Cases")
                cases = supabase.table("lawyer_cases").select("*").eq("lawyer_id", lawyer["id"]).execute().data
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

                st.markdown("### 💬 Take Action")
                colA, colB, colC = st.columns(3)
                with colA:
                    if st.button(f"📞 Call {lawyer['name'].split()[0]}", key=f"act_call_{lawyer['id']}"):
                        st.success(f"📞 Calling {lawyer['phone']}...")

                with colB:
                    st.markdown(
                        f"<a href='{wa_link}' target='_blank' style='display: block; text-align: center; background: #10B981; color: white; padding: 0.5rem; border-radius: 8px; text-decoration: none;'>💬 WhatsApp</a>",
                        unsafe_allow_html=True
                    )

                with colC:
                    if st.button(f"📅 Book ₹99 Consult", key=f"book_{lawyer['id']}"):
                        st.success("✅ Booking confirmed! You'll be contacted shortly.")

            st.divider()

    # --- PAGINATION CONTROLS ---
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if current_page > 1:
            if st.button("⬅️ Previous", key="prev_btn"):
                st.session_state.lawyers_page -= 1
                st.rerun()

    with col2:
        st.markdown(
            f"<p style='text-align: center; margin: 0; padding: 0.5rem;'>Page {current_page} of {total_pages}</p>",
            unsafe_allow_html=True
        )

    with col3:
        if current_page < total_pages:
            if st.button("Next ➡️", key="next_btn"):
                st.session_state.lawyers_page += 1
                st.rerun()

# Render
show()