# pages/db_test.py
import streamlit as st
from utils.llm import get_api_key_from_db, get_llm
import psycopg2
from contextlib import contextmanager

# --- REUSE YOUR DB CONFIG ---
DB_CONFIG = {
    "host": "192.168.0.110",
    "database": "stockagentdb",      # Replace with your DB name
    "user": "dbuser",            # Replace with your user
    "password": "dbuser@123",   # Replace with your password
    "port": 5432
}

@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
        yield None
    finally:
        if conn:
            conn.close()

def test_db_connection():
    try:
        with get_db_connection() as conn:
            if conn is None:
                return False
            if conn.closed == 0:
                st.success("✅ Connected to PostgreSQL database!")
                return True
            else:
                st.error("❌ Connection failed or closed.")
                return False
    except Exception as e:
        st.error(f"❌ Exception while connecting: {e}")
        return False

def test_fetch_api_key(service="nyay-pulse"):
    try:
        key = get_api_key_from_db(service)
        if key and len(key) > 10:
            st.success(f"✅ Fetched API key for `{service}` (masked): {key[:6]}...{key[-4:]}")
            return True
        else:
            st.warning("⚠️ Got empty or invalid key")
            return False
    except Exception as e:
        st.error(f"❌ Failed to fetch API key: {e}")
        return False

def test_llm(service="nyay-pulse"):
    try:
        llm = get_llm(service)
        # Try a simple call
        response = llm.invoke("Hello").content
        st.success(f"✅ LLM responded: '{response[:50]}...'")  # Show first 50 chars
        return True
    except Exception as e:
        st.error(f"❌ LLM failed: {e}")
        return False

# --- PAGE UI ---
def show():
    st.subheader("🔧 Database & LLM Health Check")

    st.markdown("### 1. Testing Database Connection...")
    db_ok = test_db_connection()

    if db_ok:
        st.markdown("### 2. Testing API Key Fetch...")
        key_ok = test_fetch_api_key("nyay-pulse")

        if key_ok:
            st.markdown("### 3. Testing LLM Initialization...")
            llm_ok = test_llm("nyay-pulse")
        else:
            llm_ok = False
    else:
        key_ok = llm_ok = False

    # Final Status
    st.divider()
    if db_ok and key_ok and llm_ok:
        st.balloons()
        st.success("🎉 All Systems Green! Ready for Production.")
    else:
        st.warning("⚠️ Some checks failed. Please fix before deploying.")

# Render
#show()