import streamlit as st
from backend.chat.chat_logic import get_chat_response

def render_chat_ui():
    """UI for chat assistant"""
    with st.container(border=True, height=650, width="stretch"):
        st.subheader("Chat Assistant")
        st.markdown(
            "Hi! I can help assess your **MicroLoan eligibility** using the 5C's of Credit model. "
            "Start by uploading your financial documents on the right panel."
        )
        st.divider()

        # Initialize chat history if empty
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": (
                        "Hello! I’m your MicroLoan Assistant 🤖.\n\n"
                        "Upload your financial documents on the right, and I’ll help interpret them "
                        "and check your loan eligibility."
                    ),
                }
            ]

        # Display chat history
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # User input
        user_input = st.chat_input("Type your message here...")

        if user_input:
            # Append user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            # Assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = get_chat_response(st.session_state.messages)
                    st.markdown(response)

            st.session_state.messages.append({"role": "assistant", "content": response})
