import streamlit as st

st.title("📊 Mock Analysis")
if "data" in st.session_state:
    st.write("Loan readiness score: **78/100**")
    st.write("Recommendation: ✅ Eligible for micro-loan")
else:
    st.warning("Upload and preview data before analysis.")
