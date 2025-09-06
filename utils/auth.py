# utils/auth.py
from supabase import create_client
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

def login_user(email, password):
    try:
        # Supabase Auth login
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user = response.user
        session = response.session

        # Get user role from `users` table
        user_data = supabase.table("users").select("role").eq("id", user.id).execute()
        if user_data.data:
            role = user_data.data[0]["role"]
            st.session_state.logged_in = True
            st.session_state.user_id = user.id
            st.session_state.email = email
            st.session_state.role = role
            st.session_state.name = user.email.split("@")[0].title()
            return True
        else:
            st.error("❌ User role not found")
            return False
    except Exception as e:
        st.error(f"❌ Login failed: {str(e)}")
        return False

def login(username, password, users):
    user = users.get(username)
    if user and user["password"] == password:
        return user
    return None

def logout():
    supabase.auth.sign_out()
    st.session_state.clear()
    st.rerun()