import streamlit as st
import openai

# Set page configuration
st.set_page_config(page_title="Eco Bestie 🌿", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Georgia', serif;
            background-color: #f5f3ec;
            color: #2f2e2d;
        }
        .stTextInput input {
            background-color: #fff8f1;
            color: #2f2e2d;
            border-radius: 8px;
            padding: 10px;
        }
        .stButton>button {
            background-color: #8fb996;
            color: white;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🌿 Your Eco Bestie")
st.write("Welcome to your sustainable living assistant! Ask anything eco-related — swaps, tips, composting, plastic-free, and more.")

# User input
user_input = st.text_input("💬 What would you like to ask?")

# Generate response using OpenAI
if user_input:
    with st.spinner("Thinking green thoughts... 🌱"):
        openai.api_key = st.secrets["OPENAI_API_KEY"]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're a friendly, helpful sustainability assistant focused on eco-living, zero waste, green tips, and conscious consumption."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=300
        )
        answer = response.choices[0].message.content
        st.markdown("### 🌸 Here's your tip:")
        st.write(answer)

# Footer
st.markdown("---")
st.caption("Created with 🌿 by The Eco Connection | Powered by Streamlit & OpenAI")
