import streamlit as st
from backend.chat_logic import get_chat_response

def render_chat_ui():
    """UI for chat assistant"""
    with st.container(border=True, height=650, width="stretch"):
        st.subheader("Chat Assistant")
        st.text(
            "To access your MicroLoan eligibility, we use the 5C's of Credit model.\n"
            "Please start by uploading your SME’s financial data on the right panel."
        )
        st.divider()

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": (
                        "Hello! I’m your MicroLoan Assistant 🤖.\n\n"
                        "To begin, please upload your financial documents on the **Upload Data** panel. "
                        "Once uploaded, I can help you interpret your results and assess your loan eligibility."
                    ),
                }
            ]

        # Display chat history
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # User input
        user_input = st.chat_input("Type your message here...")

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = get_chat_response(st.session_state.messages)
                    st.write(response)

            st.session_state.messages.append({"role": "assistant", "content": response})
