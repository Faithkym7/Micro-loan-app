import streamlit as st
from datetime import datetime

st.title("💬 Chat History (Mockup)")

# Sample chat history
chat_history = [
    {"title": "SME Credit Analysis - Jan 2025", "last_updated": datetime(2025, 1, 12)},
    {"title": "Collateral Discussion - Feb 2025", "last_updated": datetime(2025, 2, 8)},
    {"title": "Loan Application Follow-up", "last_updated": datetime(2025, 3, 2)},
]

st.text("This page shows your previous chat sessions with the MicroLoan Assistant.\nClick on a chat to view details (mockup).")
st.divider()

# Display each chat in a "card"
for chat in chat_history:
    with st.container():
        st.subheader(chat["title"])
        st.caption(f"🕒 Last updated: {chat['last_updated'].strftime('%b %d, %Y')}")
        st.button("🗂 Open Chat", key=f"open_{chat['title']}")
        st.markdown("---")  # separator between chats

# text to show its a mockup
st.info("⚠️ This is a mockup page. Chat history functionality is not yet implemented.")