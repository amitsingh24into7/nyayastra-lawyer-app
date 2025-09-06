# menu.py
import streamlit as st
from streamlit_option_menu import option_menu

def sidebar_menu():
    # Map display labels to internal keys
    label_to_key = {
        "Home": "dashboard",
        "AI Assistant": "ai",
        "Document AI": "documents",
        "Lawyer Connect": "lawyers",
        "Case Tracking": "case_tracking",
        "Legal Drafting": "document_gen"
    }
    key_to_label = {v: k for k, v in label_to_key.items()}

    # Get current page and its display label
    current_page = st.session_state.get("current_page", "dashboard")
    current_label = key_to_label.get(current_page, "🏠 Home")

    with st.sidebar:
        # --- Header with Logo & Tagline ---
        st.markdown(
            """
            <div style='padding: 1rem 0; text-align: center;'>
                <h2 style='margin: 0; color: #1E398F; font-size: 1.8rem;'>Nyastra</h2>
                <p style='margin: 0; color: #2563EB; font-size: 0.9rem; font-weight: 600;'>Pulse</p>
                <p style='margin: 0.5rem 0 0 0; color: #64748B; font-size: 0.85rem;'>Your Legal Rights, Simplified</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<hr style='margin: 0.75rem 0; border-color: #E2E8F0;'>", unsafe_allow_html=True)

        # --- User Profile ---
        if "name" in st.session_state:
            st.markdown(
                f"""
                <div style='padding: 0.75rem; background: #F1F5F9; border-radius: 12px; margin: 0.5rem 0;'>
                    <div style='display: flex; align-items: center; gap: 0.5rem;'>
                        <div style='width: 36px; height: 36px; background: #2563EB; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;'>
                            {st.session_state.name.split()[0][0]}
                        </div>
                        <div>
                            <strong style='color: #1E293B;'>{st.session_state.name}</strong><br>
                            <small style='color: #64748B;'>{st.session_state.role.title()}</small>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")

        # --- Navigation Menu ---
        selected_label = option_menu(
            menu_title=None,
            options=list(label_to_key.keys()),  # Display labels
            icons=["house", "robot", "file-earmark-text", "people", "search"],
            menu_icon="cast",
            default_index=list(label_to_key.values()).index(current_page),
            styles={
                "container": {
                    "padding": "0.25rem 0",
                    "background-color": "white"
                },
                "icon": {
                    "color": "#2563EB",
                    "font-size": "18px",
                    "width": "25px",
                    "text-align": "center"
                },
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "padding": "0.75rem 1rem",
                    "color": "#1E293B",
                    "border-radius": "8px",
                    "--hover-color": "#E0F2FE",
                    "transition": "all 0.2s ease"
                },
                "nav-link-selected": {
                    "background-color": "#2563EB",
                    "color": "white",
                    "font-weight": "600"
                },
            },
            key="main_nav_menu"  
        )

        # Convert display label back to internal key
        selected_key = label_to_key.get(selected_label)

        st.markdown("<hr style='margin: 1rem 0; border-color: #E2E8F0;'>", unsafe_allow_html=True)

        # --- Logout Button ---
        if st.button("🔐 Logout", use_container_width=True, type="secondary"):
            from app import logout
            logout()

        # --- Update current_page if changed ---
        if selected_key and selected_key != current_page:
            st.session_state.current_page = selected_key
            st.rerun()