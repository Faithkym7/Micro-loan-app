from openai import OpenAI
import streamlit as st

def get_chat_response(messages, loan_data=None):
    """Handles OpenAI chat logic for interactive Q&A, with optional loan data context."""
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])
    
    # Build system prompt
    system_content = (
        "You are a financial loan assessment assistant. "
        "You interpret user financial data using the 5Cs of Credit: "
        "Character, Capacity, Capital, Collateral, and Conditions. "
        "Be clear, insightful, and concise — respond like a professional loan officer."
    )
    
    # If loan data is present, inject it into context
    if loan_data:
        system_content += f" Current applicant scores: {loan_data}."
    
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system_content}, *messages],
            temperature=0.6,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error generating response: {e}"


def summarize_loan_data(loan_data):
    """Generate a short summary of the 5Cs based on the latest loan data."""
    if not loan_data:
        return "No loan data available yet."

    try:
        char = loan_data.get("characterScore", 0)
        cap = loan_data.get("capacityScore", 0)
        capital = loan_data.get("capitalScore", 0)
        coll = loan_data.get("collateralScore", 0)
        cond = loan_data.get("conditionScore", 0)
        final = loan_data.get("finalScore", 0)

        summary = (
            "📊 **Your 5Cs Credit Summary:**\n\n"
            f"- **Character:** {char}\n"
            f"- **Capacity:** {cap}\n"
            f"- **Capital:** {capital}\n"
            f"- **Collateral:** {coll}\n"
            f"- **Conditions:** {cond}\n\n"
            f"💯 **Final Eligibility Score:** {final}\n\n"
        )

        # Add simple advice
        if final >= 80:
            summary += "✅ Excellent! You’re a low-risk borrower — lenders would love this profile."
        elif final >= 60:
            summary += "🟡 Fair — your profile is acceptable, but there’s room for improvement (especially in liquidity or capital)."
        else:
            summary += "🔴 High risk — you’ll likely need stronger financial ratios or guarantees."

        return summary
    except Exception as e:
        return f"⚠️ Error summarizing loan data: {e}"
