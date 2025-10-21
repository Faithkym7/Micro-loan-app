import streamlit as st
from backend.Data.data_logic import process_uploaded_file

def render_data_ui():
    """Render file upload and data entry UI based on 5C's of Credit"""
    with st.container(border=True, height=650, width="stretch"):
        st.header("Upload Data")

        st.text(
            "⚠️ Please provide the required information and upload the relevant files for **each section**.\n"
            "All 5C’s must be completed before we can evaluate your eligibility."
        )
        st.divider()

        # --- Tab navigation ---
        tabs = st.tabs(["Character", "Capacity", "Capital", "Collateral", "Conditions"])

        files = {}

        # --- 1. Character ---
        with tabs[0]:
            st.subheader("1. Character")
            st.text(
                "This section evaluates your creditworthiness and reliability as a borrower.\n"
                "Please upload the following and provide references:"
            )
            files["crb_report"] = st.file_uploader("Credit Score Report (PDF)", type=["pdf"], key="crb_file")
            files["tax_cert"] = st.file_uploader("KRA Tax Compliance Certificate (CSV)", type=["csv"], key="kra_file")
            st.text_input("Supplier References (comma-separated)", key="supplier_refs")

        # --- 2. Capacity ---
        with tabs[1]:
            st.subheader("2. Capacity")
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
            st.subheader("3. Capital")
            st.text(
                "This section reviews your business's financial strength and how much you’ve invested.\n"
                "Please upload the following documents:"
            )
            files["cr12"] = st.file_uploader("CR12 Document (CSV/PDF)", type=["csv", "pdf"], key="cr12")
            files["balance_sheet_capital"] = st.file_uploader("Balance Sheet (CSV)", type=["csv"], key="balance_sheet_capital")
            files["retained_earnings"] = st.file_uploader("Statement of Retained Earnings (CSV)", type=["csv"], key="retained_earnings")

        # --- 4. Collateral ---
        with tabs[3]:
            st.subheader("4. Collateral")
            st.text(
                "Collateral refers to assets you can pledge to secure the loan.\n"
                "Please estimate and provide the following details:"
            )
            st.session_state["collateral_value"] = st.slider("Collateral value (Ksh)", 0, 250_000_000, 0, step=1_000_000)
            st.session_state["liquidation_value"] = st.slider(
                "Liquidity of collateral (1 = illiquid like land, 5 = very liquid like cash or receivables)", 
                1, 5, 1
            )

        # --- 5. Conditions ---
        with tabs[4]:
            st.subheader("5. Conditions")
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
                    st.dataframe(result["data"].head())
                elif result["status"] == "error":
                    st.error(f"❌ {name}: {result['message']}")
