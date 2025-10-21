import streamlit as st
from frontend.chat_ui import render_chat_ui
from frontend.data_ui import render_data_ui

st.set_page_config(page_title="Loan Advisor", page_icon="💰", layout="wide")

st.title("💰 Loan Advisor")

# Two-column layout
col1, col2 = st.columns([1, 1])

with col1:
    render_chat_ui()

with col2:
    render_data_ui()
