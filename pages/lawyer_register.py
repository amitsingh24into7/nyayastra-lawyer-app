import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

def show():
    st.subheader("📝 Lawyer Registration")
    st.markdown("Fill in your details to join Nyastra")

    with st.form("lawyer_register"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        gender = st.selectbox("Gender", ["male", "female", "other"])
        location = st.text_input("Location (City)")
        experience = st.number_input("Years of Experience", min_value=0, max_value=50)
        bar_id = st.text_input("Bar Council ID")
        about = st.text_area("About You")
        education = st.text_area("Education & Qualifications")
        specialization = st.multiselect(
            "Specialization",
            ["Criminal", "Family Law", "Cheque Bounce", "Property", "Divorce", "Labour Law", "Cyber Law", "IPR"]
        )
        languages = st.multiselect(
            "Languages Spoken",
            ["Hindi", "English", "Marathi", "Telugu", "Tamil", "Bengali", "Punjabi", "Gujarati"]
        )
        fee = st.number_input("Consultation Fee (₹)", min_value=50, value=99)

        uploaded_image = st.file_uploader("Upload Profile Photo", type=["jpg", "png"])

        submit = st.form_submit_button("Register")

        if submit:
            try:
                # Create auth user
                auth_response = supabase.auth.sign_up({
                    "email": email,
                    "password": f"temp_{phone[-4:]}"  # Temporary password
                })
                if auth_response.user:
                    user_id = auth_response.user.id

                    # Upload image to Supabase Storage
                    image_url = None
                    if uploaded_image:
                        bucket_name = "lawyer-profiles"
                        file_name = f"{user_id}/{uploaded_image.name}"
                        supabase.storage.from_(bucket_name).upload(file_name, uploaded_image.getvalue())
                        image_url = supabase.storage.from_(bucket_name).get_public_url(file_name)

                    # Insert into lawyers table
                    supabase.table("lawyers").insert({
                        "user_id": user_id,
                        "name": name,
                        "email": email,
                        "phone": phone,
                        "gender": gender,
                        "profile_image_url": image_url,
                        "specialization": specialization,
                        "location": location,
                        "experience_years": experience,
                        "about": about,
                        "education": education,
                        "bar_council_id": bar_id,
                        "languages": languages,
                        "consultation_fee": fee
                    }).execute()

                    st.success("✅ Registration successful! Admin will verify you soon.")
            except Exception as e:
                st.error(f"❌ Registration failed: {str(e)}")