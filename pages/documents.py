import streamlit as st
from utils.llm import get_llm
from PyPDF2 import PdfReader
import io

def show():
    st.subheader("📑 Nyastra Document AI")
    st.markdown("Upload a legal document (PDF) for AI-powered summary, law matching, and Q&A")

    if "doc_text" not in st.session_state:
        st.session_state.doc_text = ""
        st.session_state.doc_summary = ""
        st.session_state.doc_qa = []

    uploaded_file = st.file_uploader("Upload PDF", type="pdf", key="doc_uploader")

    if st.session_state.doc_text:
        st.info(f"📄 Currently loaded: *{getattr(uploaded_file, 'name', 'Uploaded Document')}*")
        if st.button("❌ Clear Document"):
            st.session_state.doc_text = ""
            st.session_state.doc_summary = ""
            st.session_state.doc_qa = []
            st.rerun()

    if uploaded_file and not st.session_state.doc_text:
        try:
            pdf_reader = PdfReader(io.BytesIO(uploaded_file.read()))
            raw_text = "".join(page.extract_text() + "\n" for page in pdf_reader.pages)
            st.session_state.doc_text = raw_text
            st.success(f"✅ '{uploaded_file.name}' loaded!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error processing PDF: {str(e)}")

    if st.session_state.doc_text:
        if not st.session_state.doc_summary:
            if st.button("🔍 Generate AI Summary"):
                with st.spinner("Analyzing document..."):
                    try:
                        llm = get_llm()
                        prompt = f"""
                        Summarize this legal document in simple English and Hindi.
                        Highlight: parties, court, dates, key facts, legal issues.
                        Also, suggest relevant Indian laws (IPC, CrPC, CPC, NI Act).
                        Document: {st.session_state.doc_text[:10000]}
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

        st.divider()
        st.markdown("### ❓ Ask About This Document")

        for msg in st.session_state.doc_qa:
            st.chat_message(msg["role"]).write(msg["content"])

        if q := st.chat_input("Ask a question about this document...", key="doc_qa_input"):
            st.session_state.doc_qa.append({"role": "user", "content": q})
            st.chat_message("user").write(q)
            try:
                llm = get_llm()
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