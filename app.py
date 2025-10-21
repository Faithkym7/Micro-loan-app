import streamlit as st

st.set_page_config(page_title="MicroLoan App", page_icon="💰", layout="wide")

# Create a single centered column
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.title("💰 Micro-Loan Eligibility App")

    st.markdown(
        """
        <div style="text-align: center; font-family: 'Arial', sans-serif; color: #111; line-height: 1.6;">
            <p style="font-size: 18px; margin-top: 10px;">
                Welcome! This app evaluates your <strong>MicroLoan eligibility</strong> using the <strong>5C's of Credit model</strong>.
            </p>
            <h2 style="color: #27ae60; margin-top: 30px;">How to use this app:</h2>
            <ol style="font-size: 20px; text-align: left; display: inline-block; margin-top: 15px;">
                <li>Upload your SME’s financial documents on the right panel.</li>
                <li>Use the Chat Assistant to get insights and interpret your results.</li>
                <li>Follow instructions in the chat to assess loan eligibility.</li>
            </ol>
            <p style="margin-top: 30px; font-size: 16px;">
                <b>Click the button below to start your Loan Advisor session.</b>
            </p>
        </div>

        """,
        unsafe_allow_html=True
    )

    # Center the button
    start_col1, start_col2, start_col3 = st.columns([1, 1, 1])
    with start_col2:
        if st.button("🚀 Start Loan Advisor"):
            st.switch_page("pages/01_new_chat_ui.py")
