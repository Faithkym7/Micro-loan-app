import streamlit as st
import pandas as pd

st.title("📤 Upload Data")
uploaded_file = st.file_uploader("Upload your SME financial CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state["data"] = df
    st.success("File uploaded and stored in session.")
