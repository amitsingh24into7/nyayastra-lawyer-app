# llm.py
from langchain_groq import ChatGroq
import os
import psycopg2
from contextlib import contextmanager

# Database config - Move to .env later if needed
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
        print(f"❌ Database connection failed: {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_api_key_from_db(service: str) -> str:
    """
    Fetch API key from PostgreSQL api_keys table by service name
    """
    query = "SELECT api_key FROM api_keys WHERE service = %s;"
    
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (service,))
                result = cur.fetchone()
                if result:
                    return result[0]  # Return the api_key
                else:
                    raise ValueError(f"No API key found for service: {service}")
    except Exception as e:
        print(f"❌ Failed to fetch API key for {service}: {e}")
        # Optional: Fallback to environment variable
        fallback = os.getenv("GROQ_API_KEY")
        if fallback:
            print("✅ Falling back to GROQ_API_KEY from .env")
            return fallback
        else:
            raise RuntimeError("No API key available and no fallback.")

def get_llm(service: str = "nyay-general"):
    """
    Get LLM instance with API key dynamically loaded from DB
    Use different services: nyay-pulse, nyay-client, nyay-admin, etc.
    """
    try:
        api_key = get_api_key_from_db(service)
        llm = ChatGroq(
            groq_api_key=api_key,
            model_name="llama-3.3-70b-versatile",
            temperature=0.5,
            max_tokens=1024
        )
        return llm
    except Exception as e:
        raise RuntimeError(f"Failed to initialize LLM for {service}: {e}")