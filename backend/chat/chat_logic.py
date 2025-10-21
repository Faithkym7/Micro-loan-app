from openai import OpenAI
import streamlit as st

def get_chat_response(messages):
    """Handles all OpenAI chat logic."""
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {e}"
