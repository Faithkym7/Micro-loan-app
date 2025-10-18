import streamlit as st
import pandas as pd

st.title("👀 Preview Data")
if "data" in st.session_state:
    df = st.session_state["data"]
    st.dataframe(df.head())
    st.write("Basic Stats:")
    st.write(df.describe())
else:
    st.warning("Please upload data first.")
