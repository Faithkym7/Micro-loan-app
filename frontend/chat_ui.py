import streamlit as st
from backend.chat.chat_logic import get_chat_response, summarize_loan_data

def render_chat_ui():
    """Main chat UI for the MicroLoan Assistant."""
    with st.container(border=True, height=650, width="stretch"):
        st.subheader("💬 MicroLoan Assistant")

        st.markdown(
            "Hi! I can help assess your **MicroLoan eligibility** using the 5C’s of Credit model. "
            "Upload your financials on the right, and I’ll break them down for you."
        )

        st.divider()

        # --- Initialize chat history ---
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": (
                        "👋 Hello! I’m your MicroLoan Assistant.\n\n"
                        "Upload your financial documents on the right, and I’ll analyze them "
                        "using the 5Cs of Credit (Character, Capacity, Capital, Collateral, and Conditions)."
                    ),
                }
            ]

        # --- Auto-inject latest loan summary ---
        loan_data = st.session_state.get("latest_loan_data")
        if loan_data and not any("Credit Summary" in msg["content"] for msg in st.session_state.messages):
            summary = summarize_loan_data(loan_data)
            st.session_state.messages.append({"role": "assistant", "content": summary})

        # --- Display chat history ---
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # --- User input ---
        user_input = st.chat_input("Type your question here...")

        if user_input:
            # Append user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            # Generate assistant response (inject loan data context if available)
            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    response = get_chat_response(
                        st.session_state.messages,
                        loan_data=st.session_state.get("latest_loan_data")
                    )
                    st.markdown(response)

            # Store assistant response
            st.session_state.messages.append({"role": "assistant", "content": response})
