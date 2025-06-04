
import streamlit as st
from openai import OpenAI
from openai.types.error import RateLimitError

# Page configuration
st.set_page_config(page_title="Eco Bestie 🌿", layout="centered")

# Apply custom CSS for styling
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

# Title and sidebar toggle
st.title("🌿 Your Eco Bestie")
st.write("Ask me anything about sustainable living, zero waste, eco-friendly swaps, and more.")
test_mode = st.sidebar.checkbox("🧪 Test Mode (no API call)", value=False)

# User input
user_input = st.text_input("💬 What would you like to ask?")

# Response handling
if user_input:
    if test_mode:
        st.info("🧪 Test mode is ON — no credits used.")
        st.markdown("### 🌸 Here's your mock tip:")
        st.write("Try switching to shampoo bars or refill stations instead of plastic bottles — they’re low waste and long-lasting! 💚")
    else:
        with st.spinner("Thinking green thoughts... 🌱"):
            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You're a kind, empowering sustainability coach who offers practical advice about green living, eco swaps, natural products, composting, low-waste lifestyle, and climate-conscious choices. Keep answers friendly, concise, and helpful."},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.7,
                    max_tokens=300
                )
                answer = response.choices[0].message.content
                st.markdown("### 🌸 Here's your tip:")
                st.write(answer)
            except RateLimitError:
                st.warning("🚫 We're taking a little break — too many questions at once! Please wait a minute and try again 🌿")
            except Exception as e:
                st.error("Something went wrong.")
                st.code(str(e))

# Footer
st.markdown("---")
st.caption("Created with 🌿 by The Eco Connection | Made with love by Maressa Benz")
