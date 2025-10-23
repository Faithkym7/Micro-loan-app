# data upload ui
import streamlit as st
from backend.Data.data_logic import process_uploaded_file, submit_loan_application

def render_data_ui():
    """Render file upload and data entry UI based on 5C's of Credit"""
    with st.container(border=True, height=650, width="stretch"):
        st.subheader("Upload Data")

        st.text(
            "⚠️ Please provide the required information and upload the relevant files for each section.\n"
            "All 5C’s must be completed before we can evaluate your eligibility."
        )
        with st.container(height=450, border=False):
            # --- Tab navigation ---
            tabs = st.tabs(["Character", "Capacity", "Capital", "Collateral", "Conditions"])

            files = {}

            # --- 1. Character ---
            with tabs[0]:
                st.text(
                    "This section evaluates your creditworthiness and reliability as a borrower.\n"
                    "Please upload the following and provide references:"
                )
                files["crb_report"] = st.file_uploader("Credit Score Report (PDF)", type=["pdf"], key="crb_file")
                files["tax_cert"] = st.file_uploader("KRA Tax Compliance Certificate (PDF)", type=["pdf"], key="kra_file")
                st.text_input("Supplier References (comma-separated)", key="supplier_refs")

            # --- 2. Capacity ---
            with tabs[1]:
                st.text(
                    "This section measures your ability to repay the loan.\n"
                    "Upload all the following financial statements and indicate audit status:"
                )
                files["balance_sheet"] = st.file_uploader("Recent Balance Sheet", type=["csv"], key="balance_sheet")
                files["income_statement"] = st.file_uploader("Income Statement", type=["csv"], key="income_statement")
                files["cash_flow"] = st.file_uploader("Cash Flow Statement", type=["csv"], key="cash_flow")
                files["equity_changes"] = st.file_uploader("Statement of Changes in Equity", type=["csv"], key="equity_changes")
                files["notes"] = st.file_uploader("Supporting Notes", type=["csv"], key="supporting_notes")
                # Radio for audit status
                st.radio("Are the financial statements audited?", ["Yes", "No"], key="audited")


            # --- 3. Capital ---
            with tabs[2]:
                st.text(
                    "This section reviews your business's financial strength and how much you’ve invested.\n"
                    "Please upload the following documents:"
                )
                files["cr12"] = st.file_uploader("CR12 Document (CSV/PDF)", type=["csv", "pdf"], key="cr12")
                files["balance_sheet_capital"] = st.file_uploader("Balance Sheet (CSV)", type=["csv"], key="balance_sheet_capital")
                files["retained_earnings"] = st.file_uploader("Statement of Retained Earnings (CSV)", type=["csv"], key="retained_earnings")

            # --- 4. Collateral ---
            with tabs[3]:
                st.text(
                    "Collateral refers to assets you can pledge to secure the loan.\n"
                    "Please estimate and provide the following details:"
                )
                st.session_state["collateral_value"] = st.number_input("Collateral value (Ksh)", min_value=0, step=100000)
                st.session_state["liquidation_value"] = st.slider(
                    "Liquidity of collateral (1 = illiquid like land, 5 = very liquid like cash or receivables)", 
                    1, 5, 1
                )

            # --- 5. Conditions ---
            with tabs[4]:
                st.text(
                    "This section captures the loan terms and external factors affecting repayment.\n"
                    "Please complete all fields below:"
                )
                st.session_state["loan_amount"] = st.number_input("Loan amount (Ksh)", min_value=0, step=1000)
                st.session_state["interest_rate"] = st.number_input("Interest rate (%)", min_value=0.0, step=0.1)
                st.session_state["loan_term"] = st.number_input("Loan term (months)", min_value=1, step=1)
                st.session_state["loan_purpose"] = st.text_area("Purpose of the loan")

            # --- Process uploads ---
            uploaded_any = any(files.values())
            if uploaded_any:
                results = process_uploaded_file(files)
                for name, result in results.items():
                    if result["status"] == "success":
                        st.success(f"✅ {name.replace('_', ' ').title()} uploaded successfully!")
                        data = result.get("data")
                        # Only attempt to preview tabular data (e.g., pandas DataFrame)
                        if data is not None and hasattr(data, "head"):
                            try:
                                st.dataframe(data.head())
                            except Exception:
                                st.info("Uploaded successfully but preview could not be rendered.")
                        elif data is None:
                            # Common for PDF uploads or acknowledged but non-parsed files
                            st.info("Uploaded successfully but no tabular preview is available (e.g. PDF or empty file).")
                        else:
                            # Fallback: attempt to show whatever was returned
                            try:
                                st.write(data)
                            except Exception:
                                st.info("Uploaded successfully but preview not available.")
                    elif result["status"] == "error":
                        st.error(f"❌ {name}: {result['message']}")

        if st.button("Submit"):
            # --- Filter out None files ---
            files_to_send = {k: v for k, v in files.items() if v is not None}

            # --- Build metadata ---
            metadata = {
                "character": {"supplier_refs": st.session_state.get("supplier_refs")},
                "capacity": {"audited": st.session_state.get("audited")},
                "collateral": {
                    "value": st.session_state.get("collateral_value"),
                    "liquidation_value": st.session_state.get("liquidation_value"),
                },
                "conditions": {
                    "loan_amount": st.session_state.get("loan_amount"),
                    "interest_rate": st.session_state.get("interest_rate"),
                    "loan_term": st.session_state.get("loan_term"),
                    "loan_purpose": st.session_state.get("loan_purpose"),
                },
                "uploaded_files": list(files_to_send.keys()),  # optional: track which files were uploaded
            }

            # --- Validate required fields ---
            required_fields = ["loan_amount", "interest_rate", "loan_term", "loan_purpose"]
            missing = [f for f in required_fields if st.session_state.get(f) in [None, "", 0]]
            if missing:
                st.error(f"Please fill in all required fields: {', '.join(missing)}")
            else:
                # --- Submit to n8n ---
                with st.spinner("Submitting loan application..."):
                    result = submit_loan_application(files_to_send, metadata)

                if result.get("status") == "processing":
                    st.info("✅ Your application has been received and is being processed!")
                elif result.get("status") == "success":
                    st.success("✅ Loan application submitted successfully!")
                else:
                    st.error(f"❌ Submission failed: {result.get('message')}")

                # --- Optional warning for missing optional files ---
                missing_files = [name for name, file in files.items() if file is None]
                if missing_files:
                    st.warning(f"⚠️ You didn’t upload the following optional files: {', '.join(missing_files)}")
