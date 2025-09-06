import os
import streamlit as st
from streamlit_option_menu import option_menu
from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

# --- SET PAGE CONFIG ---
st.set_page_config(
    page_title="Nyastra Pulse",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LOAD ENV VARIABLES ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --- HARD-CODED USERS ---
users = {
    "amit": {"password": "1234", "name": "Amit Kumar", "role": "admin"},
    "lawyer1": {"password": "abcd", "name": "Adv. Sharma", "role": "lawyer"},
    "client1": {"password": "pass", "name": "Rohit", "role": "client"}
}
# Add this at the top (below users)
lawyers_db = [
    {
        "name": "Adv. Priya Mehta",
        "specialization": "Cheque Bounce",
        "location": "Delhi",
        "experience": 8,
        "rating": 4.9,
        "phone": "+919876543210"
    },
    {
        "name": "Adv. Rajesh Kumar",
        "specialization": "Criminal",
        "location": "Delhi",
        "experience": 12,
        "rating": 4.8,
        "phone": "+919876543211"
    },
    {
        "name": "Adv. Anjali Reddy",
        "specialization": "Family Law",
        "location": "Hyderabad",
        "experience": 7,
        "rating": 4.7,
        "phone": "+919876543212"
    },
    {
        "name": "Adv. Arun Patel",
        "specialization": "Property",
        "location": "Mumbai",
        "experience": 10,
        "rating": 4.6,
        "phone": "+919876543213"
    },
]

# --- SESSION STATE FOR LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.name = ""
    st.session_state.role = ""

# --- LOGIN LOGIC ---
def login(username, password):
    user = users.get(username)
    if user and user["password"] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.name = user["name"]
        st.session_state.role = user["role"]
        st.rerun()
    else:
        st.error("❌ Invalid username or password")

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.name = ""
    st.session_state.role = ""
    st.rerun()

# --- CUSTOM CSS ---
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #f9fafb 0%, #f1f5f9 100%);
    }
    .sidebar .sidebar-content {
        background: #1e3a8a;
        color: white;
    }
    .css-1d391kg {
        padding: 2rem 1rem;
    }
    .stButton>button {
        border-radius: 8px;
        height: 3rem;
    }
    .st-emotion-cache-1kyxreq {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- SHOW LOGIN OR APP ---
if not st.session_state.logged_in:
    # --- LOGIN SCREEN ---
    st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>⚖️ Nyastra Pulse</h1>", unsafe_allow_html=True)
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

else:
    # --- AFTER LOGIN ---
    with st.sidebar:
        st.markdown(
            f"<h3 style='color: white; text-align: center;'>👋 Hello, {st.session_state.name}</h3>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<p style='color: #e0f2fe; text-align: center;'>Role: {st.session_state.role.title()}</p>",
            unsafe_allow_html=True
        )
        st.divider()

        # --- Initialize Session State (Persistent Across Navigation) ---
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        if "doc_text" not in st.session_state:
            st.session_state.doc_text = ""

        if "doc_summary" not in st.session_state:
            st.session_state.doc_summary = ""

        if "doc_qa" not in st.session_state:
            st.session_state.doc_qa = []
        # --- OPTION MENU ---
        selected = option_menu(
            menu_title="Main Menu",
            options=["dashboard", "ai", "documents", "lawyers"],
            icons=["house", "robot", "file-earmark-text", "people"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#1e3a8a"},
                "icon": {"color": "#e0f2fe", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "color": "#e0f2fe",
                    "padding": "10px 20px",
                    "border-radius": "8px",
                    "--hover-color": "#1e40af"
                },
                "nav-link-selected": {"background-color": "#2563eb"},
            }
        )

        st.divider()
        if st.button("🔐 Logout", use_container_width=True):
            logout()

    # --- DASHBOARD ---
    if selected == "dashboard":
        st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>Nyastra Pulse</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #2563EB;'>Your Legal Rights, Simplified</h3>", unsafe_allow_html=True)
        st.markdown("---")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("✅ Track Your Case")
            st.caption("Get real-time updates from eCourts")
        with col2:
            st.info("🤖 AI Legal Help")
            st.caption("Ask in Hindi or English")
        with col3:
            st.info("📞 Talk to a Lawyer")
            st.caption("₹99 for 15-min consult")

        if st.session_state.role == "admin":
            st.success("🧑‍💼 Admin Panel: Manage users, cases, AI")
        elif st.session_state.role == "lawyer":
            st.success("👨‍⚖️ Lawyer Mode: View clients, cases")
        elif st.session_state.role == "client":
            st.success("🎯 You're all set! Start with AI or document upload")

    # --- LEGAL ASSISTANT ---
    elif selected == "ai":
        st.subheader("🤖 Nyastra AI Legal Assistant")
        st.markdown("Ask any legal question in **Hindi or English**")

        # Display chat history
        for msg in st.session_state.chat_history:
            st.chat_message(msg["role"]).write(msg["content"])

        # Input
        if prompt := st.chat_input("Ask a legal question...", key="ai_chat_input"):
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)

            try:
                from langchain_groq import ChatGroq
                llm = ChatGroq(
                    groq_api_key=os.getenv("GROQ_API_KEY"),
                    model_name="llama3-8b-8192",
                    temperature=0.5,
                    max_tokens=512
                )

                # System context
                system_prompt = "You are Nyastra, a helpful Indian legal assistant. Answer in simple Hindi or English. Cite laws (IPC, CrPC, NI Act). If unsure, say 'Consult a lawyer.'"

                messages = [
                    {"role": "system", "content": system_prompt}
                ] + st.session_state.chat_history

                response = llm.invoke(messages)
                assistant_msg = response.content

                # Save and display
                st.session_state.chat_history.append({"role": "assistant", "content": assistant_msg})
                st.chat_message("assistant").write(assistant_msg)

            except Exception as e:
                error_msg = f"AI Error: {str(e)}"
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
                st.chat_message("assistant").write(error_msg)

    # --- DOCUMENT TOOLS ---
    elif selected == "documents":
        st.subheader("📑 Nyastra Document AI")
        st.markdown("Upload a legal document (PDF) for AI-powered summary, law matching, and Q&A")

        uploaded_file = st.file_uploader("Upload PDF", type="pdf", key="doc_uploader")

        # Show current document status
        if st.session_state.doc_text:
            st.info(f"📄 Currently loaded: *{getattr(uploaded_file, 'name', 'Uploaded Document')}*")
            if st.button("❌ Clear Document"):
                st.session_state.doc_text = ""
                st.session_state.doc_summary = ""
                st.session_state.doc_qa = []
                st.rerun()

        if uploaded_file and not st.session_state.doc_text:
            from PyPDF2 import PdfReader
            import io

            try:
                pdf_reader = PdfReader(io.BytesIO(uploaded_file.read()))
                raw_text = ""
                for page in pdf_reader.pages:
                    raw_text += page.extract_text() + "\n"

                st.session_state.doc_text = raw_text
                st.success(f"✅ '{uploaded_file.name}' loaded!")

                # Rerun to show document UI
                st.rerun()

            except Exception as e:
                st.error(f"❌ Error processing PDF: {str(e)}")

        # If document is loaded, show AI tools
        if st.session_state.doc_text:
            # AI Summary
            if not st.session_state.doc_summary:
                if st.button("🔍 Generate AI Summary"):
                    with st.spinner("Analyzing document..."):
                        try:
                            from langchain_groq import ChatGroq
                            llm = ChatGroq(
                                groq_api_key=os.getenv("GROQ_API_KEY"),
                                model_name="llama3-8b-8192",
                                temperature=0.5,
                                max_tokens=1024
                            )

                            prompt = f"""
                            Summarize this legal document in simple English and Hindi.
                            Highlight: parties, court, dates, key facts, legal issues.
                            Also, suggest relevant Indian laws (IPC, CrPC, CPC, NI Act).

                            Document:
                            {st.session_state.doc_text[:10000]}
                            """

                            response = llm.invoke([{"role": "user", "content": prompt}])
                            st.session_state.doc_summary = response.content
                            st.info("📌 **AI Summary & Laws Found**")
                            st.write(st.session_state.doc_summary)

                        except Exception as e:
                            st.error(f"❌ Summary failed: {str(e)}")

            else:
                st.info("📌 **AI Summary & Laws Found**")
                st.write(st.session_state.doc_summary)

            # Q&A Section
            st.divider()
            st.markdown("### ❓ Ask About This Document")

            # Display Q&A history
            for msg in st.session_state.doc_qa:
                st.chat_message(msg["role"]).write(msg["content"])

            # Input
            if q := st.chat_input("Ask a question about this document...", key="doc_qa_input"):
                st.session_state.doc_qa.append({"role": "user", "content": q})
                st.chat_message("user").write(q)

                try:
                    from langchain_groq import ChatGroq
                    llm = ChatGroq(
                        groq_api_key=os.getenv("GROQ_API_KEY"),
                        model_name="llama3-8b-8192",
                        temperature=0.3,
                        max_tokens=512
                    )

                    prompt = f"""
                    Based on this legal document:
                    {st.session_state.doc_text[:5000]}

                    Question: {q}
                    Answer in simple English or Hindi. Cite sections if possible.
                    """

                    response = llm.invoke([{"role": "user", "content": prompt}])
                    answer = response.content

                    st.session_state.doc_qa.append({"role": "assistant", "content": answer})
                    st.chat_message("assistant").write(answer)

                except Exception as e:
                    error = f"❌ AI Error: {str(e)}"
                    st.session_state.doc_qa.append({"role": "assistant", "content": error})
                    st.chat_message("assistant").write(error)
                    # --- LAWYER CONNECT ---
    elif selected == "lawyers":
        st.subheader("📞 Find a Verified Lawyer")
        st.markdown("Search by location and specialization")

        # Filters
        col1, col2 = st.columns(2)
        with col1:
            location = st.selectbox("📍 Location", ["All", "Delhi", "Mumbai", "Hyderabad", "Bangalore"])
        with col2:
            spec = st.selectbox("🎯 Specialization", 
                            ["All", "Criminal", "Cheque Bounce", "Family Law", "Property", "Divorce", "Labour Law"])

        # Filter lawyers
        filtered = lawyers_db
        if location != "All":
            filtered = [l for l in filtered if l["location"] == location]
        if spec != "All":
            filtered = [l for l in filtered if l["specialization"] == spec]

        if not filtered:
            st.warning("No lawyers found for selected filters.")
        else:
            for lawyer in filtered:
                with st.container():
                    st.markdown(f"### {lawyer['name']}")
                    st.markdown(f"**Specialization:** {lawyer['specialization']} | **Location:** {lawyer['location']}")
                    st.markdown(f"**Experience:** {lawyer['experience']} years | ⭐ {lawyer['rating']}")
                    
                    colA, colB = st.columns(2)
                    with colA:
                        if st.button(f"📞 Call {lawyer['name'].split()[1]}", key=f"call_{lawyer['name']}"):
                            st.success(f"Calling {lawyer['phone']}...")
                    with colB:
                        if st.button(f"💬 WhatsApp", key=f"wa_{lawyer['name']}"):
                            wa_link = f"https://wa.me/{lawyer['phone'].replace('+', '')}?text=Hi, I need legal help"
                            st.markdown(f"[Open WhatsApp Chat]({wa_link})", unsafe_allow_html=True)
                    st.divider()

# --- FOOTER ---
st.divider()
st.markdown(
    "<p style='text-align: center; color: #64748B;'>Nyastra • Know your case. Take action.</p>",
    unsafe_allow_html=True
)