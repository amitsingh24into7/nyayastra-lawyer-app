import streamlit as st

def show():
    st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>Nyastra Pulse</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #2563EB;'>Your Legal Rights, Simplified</h3>", unsafe_allow_html=True)
    st.markdown("---")
    # Initialize session state for balloons
    if 'balloons_shown' not in st.session_state:
        st.session_state.balloons_shown = False    
    

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

    role = st.session_state.role
    if role == "admin":
        st.success("🧑‍💼 Admin Panel: Manage users, cases, AI")
    elif role == "lawyer":
        st.success("👨‍⚖️ Lawyer Mode: View clients, cases")
    elif role == "client":
        st.success("🎯 You're all set! Start with AI or document upload")

    if not st.session_state.balloons_shown:
                st.balloons()
                st.session_state.balloons_shown = True  # Mark as shown                