import streamlit as st
from utils.llm import get_llm

def show():
    st.subheader("🤖 Nyastra AI Legal Assistant")
    st.markdown("Ask any legal question in **Hindi or English**")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat
    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["content"])

    # Input
    if prompt := st.chat_input("Ask a legal question...", key="ai_chat_input"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        try:
            llm = get_llm('nyay-pulse')
            system_prompt = "You are Nyastra, a helpful Indian legal assistant. Answer in simple Hindi or English. Cite laws (IPC, CrPC, NI Act). If unsure, say 'Consult a lawyer.'"
            messages = [{"role": "system", "content": system_prompt}] + st.session_state.chat_history
            response = llm.invoke(messages)
            assistant_msg = response.content
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_msg})
            st.chat_message("assistant").write(assistant_msg)
        except Exception as e:
            error = f"❌ AI Error: {str(e)}"
            st.session_state.chat_history.append({"role": "assistant", "content": error})
            st.chat_message("assistant").write(error)