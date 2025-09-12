import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv
load_dotenv()

# --- SET PAGE CONFIG ---
st.set_page_config(
    page_title="Nyayastra Pulse",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- HARD-CODED USERS ---
users = {
    "amit": {"password": "1234", "name": "Amit Kumar", "role": "admin"},
    "lawyer1": {"password": "abcd", "name": "Adv. Sharma", "role": "lawyer"},
    "client1": {"password": "pass", "name": "Rohit", "role": "client"}
}

# --- SESSION STATE FOR LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.name = ""
    st.session_state.role = ""
    st.session_state.current_page = "dashboard"  # Default page

# --- LOGIN LOGIC ---
def login(username, password):
    user = users.get(username)
    if user and user["password"] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.name = user["name"]
        st.session_state.role = user["role"]
        st.session_state.current_page = "dashboard"
        st.rerun()
    else:
        st.error("❌ Invalid username or password")

def logout():
    st.session_state.logged_in = False
    st.session_state.clear()
    st.rerun()

# --- CUSTOM CSS: Hide Default Sidebar Navigation ---
st.markdown(
    """
    <style>
    /* Hide the auto-generated page navigation */
    div[data-testid="stSidebarNav"] { display: none !important; }
    /* Custom sidebar styling */
    .main { background: linear-gradient(135deg, #f9fafb 0%, #f1f5f9 100%); }
    .css-1d391kg { padding: 2rem 1rem; }
    .stButton>button { border-radius: 8px; height: 3rem; }
    </style>
    """,
    unsafe_allow_html=True
)

# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>⚖️ Nyayastra Pulse</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem;'>India's AI-Powered Legal Assistant</p>", unsafe_allow_html=True)
    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.text_input("Username", key="username_input")
            st.text_input("Password", type="password", key="password_input")
            submit = st.form_submit_button("🔐 Login", use_container_width=True)
            if submit:
                login(st.session_state.username_input, st.session_state.password_input)
            st.markdown(
    """
    <div style="padding: 0.5rem 1rem;">
        <a href="https://forms.gle/your-lawyer-registration-form-link" target="_blank" style="text-decoration: none;">
            <div style="
                background: #2563EB;
                color: white;
                padding: 0.75rem;
                border-radius: 12px;
                text-align: center;
                font-weight: 600;
                font-size: 14px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                📝 Register as a Lawyer
            </div>
        </a>
    </div>
    <p style="text-align: center; color: #64748B; margin-top: 1rem;">
        Nyayastra • Know your case. Take action.
    </p>
    """,
    unsafe_allow_html=True
)
    st.stop()

# --- AFTER LOGIN ---
# Import and call sidebar menu (it will handle navigation)
from menu import sidebar_menu
sidebar_menu()  # This will show custom menu and hide default nav

# --- LOAD SELECTED PAGE ---
selected = st.session_state.current_page

try:
    if selected == "dashboard":
        from pages.dashboard import show
    elif selected == "ai":
        from pages.ai_chat import show
    elif selected == "documents":
        from pages.documents import show
    elif selected == "lawyers":
        from pages.lawyers import show
    elif selected == "case_tracking":
        from pages.case_tracking import show
    elif selected == "document_gen":
        from pages.document_gen import show
    elif selected == "db_test":
        from pages.db_test import show
    else:
        from pages.dashboard import show  # fallback

    # Add fade-in to page content
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    show()
    st.markdown("</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"❌ Failed to load page: {str(e)}")

# --- FOOTER ---
st.divider()
st.markdown(
    "<p style='text-align: center; color: #64748B;'>Nyayastra • Know your case. Take action.</p>",
    unsafe_allow_html=True
)