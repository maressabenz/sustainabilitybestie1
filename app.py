import streamlit as st
import openai

st.set_page_config(page_title="Eco Bestie 🌿", layout="centered")

# Styles...
# (keep your CSS as-is)

st.title("🌿 Your Eco Bestie")
st.write("Welcome to your sustainable living assistant! Ask anything eco-related — swaps, tips, composting, plastic-free, and more.")

user_input = st.text_input("💬 What would you like to ask?")

if user_input:
    with st.spinner("Thinking green thoughts... 🌱"):
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
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

st.markdown("---")
st.caption("Created with 🌿 by The Eco Connection | Maressa Benz")

