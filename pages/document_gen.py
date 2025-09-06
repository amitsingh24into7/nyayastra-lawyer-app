# pages/document_gen.py
import os
# Optional: Only if using WeasyPrint with custom DLL path
# os.environ["WEASYPRINT_DLL_DIRECTORIES"] = r"D:\wkhtmltox\bin"

import streamlit as st
from datetime import datetime
from utils.pdf_generator import generate_pdf

def show():
    st.subheader("📄 Document Generator")
    st.markdown("Create court-ready legal documents in minutes")

    doc_type = st.selectbox(
        "Select Document Type",
        [
            "Cheque Bounce (Section 138 NI Act)",
            "Divorce Petition (Mutual Consent)",
            "Anticipatory Bail",
            "Residential Rent Agreement",
            "Recovery of Money Suit"
        ],
        key="doc_type_select"
    )

    # Map to template
    template_map = {
        "Cheque Bounce (Section 138 NI Act)": "ni_act_138_notice.html",
        "Divorce Petition (Mutual Consent)": "divorce_petition.html",
        "Anticipatory Bail": "anticipatory_bail.html",
        "Residential Rent Agreement": "rent_agreement.html",
        "Recovery of Money Suit": "recovery_suit.html"
    }

    if not doc_type:
        return

    st.info(f"📝 Preparing: {doc_type}")
    template_file = template_map[doc_type]

    # Input Form
    with st.form("doc_form"):
        st.markdown("### 🧾 Case Details")

        # --- Cheque Bounce ---
        if doc_type == "Cheque Bounce (Section 138 NI Act)":
            st.markdown("### 💰 Cheque & Transaction Details")

            # Client (Complainant)
            client_name = st.text_input("Client Name (Individual/Business)")
            client_address = st.text_area("Client Address")
            transaction_purpose = st.text_input("Purpose of Transaction (e.g., Sale of goods, Service rendered)")

            # Accused (Drawer)
            accused_name = st.text_input("Accused Name")
            accused_address = st.text_area("Accused Address")
            accused_pincode = st.text_input("Accused Pincode")

            # Cheque Details
            cheque_number = st.text_input("Cheque Number")
            cheque_date = st.date_input("Cheque Date")
            amount = st.number_input("Amount (₹)", min_value=1)
            amount_in_words = st.text_input("Amount in Words (e.g., Fifty Thousand Only)")

            # Bank Details
            bank_name = st.text_input("Bank Name")
            bank_branch = st.text_input("Bank Branch")
            presentation_date = st.date_input("Date of Presentation")
            return_reason = st.text_input("Return Reason (e.g., 'Insufficient Funds')")
            intimation_date = st.date_input("Date of Intimation")

            # Notice Details
            transaction_date = st.date_input("Date of Transaction")
            notice_cost = st.number_input("Notice Cost (₹)", min_value=100, value=500)
            stamp_value = st.text_input("Stamp Paper Value (₹)", value="200")
            ref_number = st.text_input("Notice Reference No.", value=f"NI/{datetime.now().strftime('%Y')}/001")
            advocate_name = st.text_input("Advocate Name (for signature)")

            submit = st.form_submit_button("Generate Document")

            if submit:
                # Validate required fields
                required_fields = [client_name, client_address, accused_name, accused_address, cheque_number]
                if not all(required_fields):
                    st.error("❌ Please fill all required fields.")
                else:
                    # Prepare data
                    data = {
                        "client_name": client_name,
                        "client_address": client_address,
                        "transaction_purpose": transaction_purpose,
                        "accused_name": accused_name,
                        "accused_address": accused_address,
                        "accused_pincode": accused_pincode,
                        "cheque_number": cheque_number,
                        "cheque_date": cheque_date.strftime("%d-%m-%Y"),
                        "amount": amount,
                        "amount_in_words": amount_in_words,
                        "bank_name": bank_name,
                        "bank_branch": bank_branch,
                        "presentation_date": presentation_date.strftime("%d-%m-%Y"),
                        "return_reason": return_reason,
                        "intimation_date": intimation_date.strftime("%d-%m-%Y"),
                        "transaction_date": transaction_date.strftime("%d-%m-%Y"),
                        "notice_cost": notice_cost,
                        "stamp_value": stamp_value,
                        "ref_number": ref_number,
                        "advocate_name": advocate_name,
                        "today": datetime.now().strftime("%d-%m-%Y")
                    }

                    # Generate PDF
                    os.makedirs("documents/generated", exist_ok=True)
                    pdf_path = f"documents/generated/cheque_bounce_{int(datetime.now().timestamp())}.pdf"
                    generate_pdf(template_file, data, pdf_path)

                    st.session_state.generated_pdf = pdf_path
                    st.session_state.doc_data = data
                    st.session_state.doc_type = doc_type
                    st.success("✅ Legal Notice Generated!")

        # --- Divorce Petition ---
        elif doc_type == "Divorce Petition (Mutual Consent)":
            st.markdown("### 👫 Marriage Details")
            petitioner_name = st.text_input("Petitioner Name")
            respondent_name = st.text_input("Respondent Name")
            marriage_date = st.date_input("Date of Marriage")
            marriage_place = st.text_input("Place of Marriage")
            separation_years = st.number_input("Years of Separation", min_value=1, max_value=20)

            submit = st.form_submit_button("Generate Document")

            if submit:
                if not petitioner_name or not respondent_name:
                    st.error("❌ Please fill all required fields.")
                else:
                    data = {
                        "petitioner_name": petitioner_name,
                        "respondent_name": respondent_name,
                        "marriage_date": marriage_date.strftime("%d-%m-%Y"),
                        "marriage_place": marriage_place,
                        "separation_years": separation_years,
                        "today": datetime.now().strftime("%d-%m-%Y")
                    }

                    os.makedirs("documents/generated", exist_ok=True)
                    pdf_path = f"documents/generated/divorce_petition_{int(datetime.now().timestamp())}.pdf"
                    generate_pdf(template_file, data, pdf_path)

                    st.session_state.generated_pdf = pdf_path
                    st.session_state.doc_data = data
                    st.session_state.doc_type = doc_type
                    st.success("✅ Divorce Petition Generated!")

        # --- Anticipatory Bail ---
        elif doc_type == "Anticipatory Bail":
            st.markdown("### ⚖️ FIR & Accusation Details")
            applicant_name = st.text_input("Applicant Name")
            fir_number = st.text_input("FIR Number")
            police_station = st.text_input("Police Station")
            ipc_sections = st.text_input("IPC Sections (e.g., 420, 467)")
            reason_for_bail = st.text_area("Reason for Seeking Bail")
            jurisdiction = st.text_input("Jurisdiction (e.g., Delhi)")

            submit = st.form_submit_button("Generate Document")

            if submit:
                if not applicant_name or not fir_number:
                    st.error("❌ Please fill all required fields.")
                else:
                    data = {
                        "applicant_name": applicant_name,
                        "fir_number": fir_number,
                        "police_station": police_station,
                        "ipc_sections": ipc_sections,
                        "reason_for_bail": reason_for_bail,
                        "jurisdiction": jurisdiction,
                        "today": datetime.now().strftime("%d-%m-%Y")
                    }

                    os.makedirs("documents/generated", exist_ok=True)
                    pdf_path = f"documents/generated/anticipatory_bail_{int(datetime.now().timestamp())}.pdf"
                    generate_pdf(template_file, data, pdf_path)

                    st.session_state.generated_pdf = pdf_path
                    st.session_state.doc_data = data
                    st.session_state.doc_type = doc_type
                    st.success("✅ Anticipatory Bail Application Generated!")

        # --- Residential Rent Agreement ---
        elif doc_type == "Residential Rent Agreement":
            st.markdown("### 🏠 Property & Agreement Details")

            # Parties
            landlord_name = st.text_input("Landlord Name")
            landlord_father_name = st.text_input("Landlord Father's Name")
            landlord_address = st.text_area("Landlord Full Address")

            tenant_name = st.text_input("Tenant Name")
            tenant_father_name = st.text_input("Tenant Father's Name")
            tenant_address = st.text_area("Tenant Full Address")
            tenant_occupation_place = st.text_input("Tenant Occupation / Study Place")

            # Property
            property_address = st.text_area("Full Property Address")
            agreement_city = st.text_input("City of Agreement (e.g., Delhi)")
            bedrooms = st.number_input("Number of Bedrooms", min_value=1)
            fans = st.number_input("Number of Fans", min_value=0)
            lights = st.number_input("Number of CFL Lights", min_value=0)
            geysers = st.number_input("Number of Geysers", min_value=0)
            mirrors = st.number_input("Number of Mirrors", min_value=0)

            # Dates
            execution_date = st.number_input("Execution Date (e.g., 15)", min_value=1, max_value=31)
            execution_month = st.text_input("Execution Month (e.g., January)")
            execution_year = st.number_input("Execution Year", min_value=2020, value=2025)
            start_date = st.date_input("Agreement Start Date")
            end_date = st.date_input("Agreement End Date")

            # Financials
            monthly_rent = st.number_input("Monthly Rent (₹)", min_value=1)
            maintenance_charge = st.number_input("Monthly Maintenance (₹)", min_value=0)
            security_deposit = st.number_input("Security Deposit (₹)", min_value=1)
            cheque_number = st.text_input("Cheque Number (Security Deposit)")
            cheque_date = st.date_input("Cheque Date")

            # Other
            jurisdiction = st.text_input("Jurisdiction (e.g., Delhi)")
            stamp_value = st.text_input("Stamp Paper Value (₹)", value="100")

            submit = st.form_submit_button("Generate Document")

            if submit:
                if not landlord_name or not tenant_name or not property_address:
                    st.error("❌ Please fill all required fields.")
                else:
                    data = {
                        "landlord_name": landlord_name,
                        "landlord_father_name": landlord_father_name,
                        "landlord_address": landlord_address,
                        "tenant_name": tenant_name,
                        "tenant_father_name": tenant_father_name,
                        "tenant_address": tenant_address,
                        "tenant_occupation_place": tenant_occupation_place,
                        "property_address": property_address,
                        "agreement_city": agreement_city,
                        "bedrooms": bedrooms,
                        "fans": fans,
                        "lights": lights,
                        "geysers": geysers,
                        "mirrors": mirrors,
                        "execution_date": execution_date,
                        "execution_month": execution_month,
                        "execution_year": execution_year,
                        "start_date": start_date.strftime("%d-%m-%Y"),
                        "end_date": end_date.strftime("%d-%m-%Y"),
                        "monthly_rent": monthly_rent,
                        "maintenance_charge": maintenance_charge,
                        "security_deposit": security_deposit,
                        "cheque_number": cheque_number,
                        "cheque_date": cheque_date.strftime("%d-%m-%Y"),
                        "jurisdiction": jurisdiction,
                        "stamp_value": stamp_value
                    }

                    os.makedirs("documents/generated", exist_ok=True)
                    pdf_path = f"documents/generated/rent_agreement_{int(datetime.now().timestamp())}.pdf"
                    generate_pdf(template_file, data, pdf_path)

                    st.session_state.generated_pdf = pdf_path
                    st.session_state.doc_data = data
                    st.session_state.doc_type = doc_type
                    st.success("✅ Rent Agreement Generated!")

        # --- Recovery of Money ---
        elif doc_type == "Recovery of Money Suit":
            st.markdown("### 💸 Loan & Recovery Details")
            plaintiff_name = st.text_input("Plaintiff Name")
            defendant_name = st.text_input("Defendant Name")
            amount = st.number_input("Amount (₹)", min_value=1)
            loan_date = st.date_input("Date of Loan")
            due_date = st.date_input("Due Date for Repayment")
            notice_date = st.date_input("Legal Notice Date")
            jurisdiction = st.text_input("Jurisdiction (e.g., Delhi)")

            submit = st.form_submit_button("Generate Document")

            if submit:
                if not plaintiff_name or not defendant_name:
                    st.error("❌ Please fill all required fields.")
                else:
                    data = {
                        "plaintiff_name": plaintiff_name,
                        "defendant_name": defendant_name,
                        "amount": amount,
                        "loan_date": loan_date.strftime("%d-%m-%Y"),
                        "due_date": due_date.strftime("%d-%m-%Y"),
                        "notice_date": notice_date.strftime("%d-%m-%Y"),
                        "jurisdiction": jurisdiction,
                        "today": datetime.now().strftime("%d-%m-%Y")
                    }

                    os.makedirs("documents/generated", exist_ok=True)
                    pdf_path = f"documents/generated/recovery_suit_{int(datetime.now().timestamp())}.pdf"
                    generate_pdf(template_file, data, pdf_path)

                    st.session_state.generated_pdf = pdf_path
                    st.session_state.doc_data = data
                    st.session_state.doc_type = doc_type
                    st.success("✅ Recovery Suit Generated!")

    # Show Generated PDF & Approval Flow
    if "generated_pdf" in st.session_state:
        st.divider()
        st.markdown("### 🔍 Review Document")
        with open(st.session_state.generated_pdf, "rb") as f:
            st.download_button(
                "⬇️ Download PDF",
                f,
                file_name=f"{st.session_state.doc_type}.pdf",
                mime="application/pdf"
            )

        st.markdown("### ✅ Client Approval")
        if st.button("✅ Approve & Confirm", key="approve_doc"):
            st.session_state.doc_approved = True
            st.success("🎉 Document approved! Ready for filing.")

        if st.session_state.get("doc_approved"):
            st.markdown("### 📬 Filing Options")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🖨️ Print & File Offline", key="print_file"):
                    st.info("You can now print and file in court.")
            with col2:
                if st.button("🌐 File Online (eCourts)", key="efile"):
                    st.info("Coming soon: Auto e-filing integration.")

# Render
show()