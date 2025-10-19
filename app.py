import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="MicroLoan Eligibility", page_icon="💰", layout="wide")

st.title("💰 Micro-Loan Eligibility App")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# Two-column layout
col1, col2 = st.columns([2, 1])

# ---------------------------
# CHAT COLUMN (left side)
# ---------------------------
with col1:
    with st.container(border=True, height=500, width="stretch"):
        st.subheader("Chat Assistant")

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! I’m your MicroLoan Assistant. How can I help you today?"}
            ]

        # Display previous messages
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # User input
        user_input = st.chat_input("Type your message here...")

        if user_input:
            # Display user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)

            # Get assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        completion = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=st.session_state.messages
                        )
                        response = completion.choices[0].message.content
                    except Exception as e:
                        response = f"⚠️ Error: {e}"

                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

# ---------------------------
# UPLOAD COLUMN (right side)
# ---------------------------
with col2:
    with st.container(border=True, height=500, width="stretch"):
        st.subheader("Upload Data")
        uploaded_file = st.file_uploader("Upload your SME financial CSV", type=["csv"])
        if uploaded_file:
            st.success("✅ File uploaded successfully!")
            st.session_state["data"] = uploaded_file
