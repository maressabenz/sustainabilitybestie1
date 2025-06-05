
import streamlit as st
import pandas as pd
from openai import OpenAI

# --- CONFIG & STYLE ---
st.set_page_config(page_title="Eco Bestie by The Eco Connection🌿", layout="wide")

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
        .eco-card {
            background-color: #ffffff;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 1rem;
        }
        .eco-link {
            font-size: 14px;
            color: #4a7c59;
            text-decoration: none;
        }
    </style>
""", unsafe_allow_html=True)

# --- LOAD DATA FROM GOOGLE SHEETS ---
@st.cache_data
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ9X4uUiJ62AowI-E41-Q3CfMP24rFpe6Amci5IdB7gWg8SBCZOX-q4B7J0zv2uXouNo5vBipwxSnKb/pub?output=csv"
    return pd.read_csv(sheet_url)

df = load_data()

products = df[df["type"] == "product"].to_dict(orient="records")
eco_tips = df[df["type"] == "eco_tip"].to_dict(orient="records")
swaps = df[df["type"] == "swap"].to_dict(orient="records")

# --- TITLE ---
st.title("Hi! I'm your Eco Bestie 🌿")
st.write("I'm here to help you live more gently with the Earth. Ask me anything about sustainability, eco-friendly swaps, or how to reconnect with nature. 🌸")

# --- USER INPUT ---
user_input = st.text_input("💬 Type in your question and press enter.")

if user_input:
    with st.spinner("Thinking green thoughts... 🌱"):
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                   {"role": "system", "content": "You are Eco Bestie, a practical and encouraging voice powered by The Eco Connection. You speak in a grounded, clear, and intentional tone — like a thoughtful friend who makes sustainable living feel approachable, empowering, and real. Avoid mystical, overly poetic, or fantasy-style language. Your job is to give relatable, educational, and kind guidance without judgment. Prioritize actionable steps, clarity, and compassion. You can be a little warm and creative, but always human, honest, and useful.You sound like a young, conscious creative who's passionate about sustainability, slow living, solarpunk, and intentional consumerism — but you're also realistic and not too idealistic. You're the kind of person someone would DM on Instagram for advice because you keep it real.
"},

                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,
                max_tokens=300
            )
            answer = response.choices[0].message.content
            st.markdown("### Here's your tip:")
            st.write(answer)
        except Exception as e:
            st.warning("🌧 Hmm... something went wrong. Try again in a bit.")
            st.code(str(e))

# --- DISPLAY CARDS ---
def render_cards(data, section_title):
    st.markdown(f"## {section_title}")
    cols = st.columns(3)
    for i, item in enumerate(data):
        with cols[i % 3]:
            # Make image clickable using separate image_link column
            image_url = item.get("image", "")
            image_link = item.get("image_link", item.get("link", ""))  # fallback to link if image_link is missing

            img_html = (
                f'<a href="{image_link}" target="_blank">'
                f'<img src="{image_url}" style="width:100%; border-radius:12px; margin-bottom:0.5rem;" />'
                f'</a>'
            ) if image_url else ""

            # Display card with image, title, description, and CTA link
            st.markdown(f"""
                <div style="background-color:#fff; padding:1rem; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.08); text-align:center;">
                    {img_html}
                    <h4>{item['emoji']} {item['title']}</h4>
                    <p>{item['desc']}</p>
                    <a href="{item['link']}" target="_blank" style="color:#4a7c59; font-weight:500;">Learn more →</a>
                </div>
            """, unsafe_allow_html=True)

            
st.markdown("---")
render_cards(products, "🛍 Thoughtful Product Recommendations")
render_cards(eco_tips, "🌱 Gentle Eco Living Tips")
render_cards(swaps, "🔁 Sustainable Swaps to Try")

st.markdown("---")
st.caption("Created by Maressa Benz | The Eco Connection")


