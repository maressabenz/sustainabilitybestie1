import streamlit as st
from openai import OpenAI

# --- CONFIG & STYLE ---
st.set_page_config(page_title="Eco Bestie 🌿", layout="wide")

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

# --- DATA ---
products = [
    {"emoji": "🧴", "title": "Shampoo Bar", "desc": "Plastic-free and nourishing.", "link": "https://youraffiliate.link/shampoo"},
    {"emoji": "🛍", "title": "Produce Bags", "desc": "Reusable cotton for grocery runs.", "link": "https://yourblog.com/produce-bags"},
    {"emoji": "🧼", "title": "Compostable Sponges", "desc": "Biodegradable & zero waste.", "link": "https://yourblog.com/kitchen-swaps"},
]

eco_tips = [
    {"emoji": "🍃", "title": "Slow Mornings", "desc": "Start your day with tea, barefoot on the earth.", "link": ""},
    {"emoji": "🌞", "title": "Line Drying", "desc": "Let the sun do the work — no dryer needed.", "link": ""},
    {"emoji": "📦", "title": "Reuse Packaging", "desc": "Boxes, jars & wrap get a second life.", "link": ""},
]

swaps = [
    {"emoji": "🥤", "title": "Bamboo Straw", "desc": "Skip plastic with a reusable straw.", "link": ""},
    {"emoji": "🧻", "title": "Cloth Napkins", "desc": "Washable and elegant at meals.", "link": ""},
    {"emoji": "🛁", "title": "Bar Soap", "desc": "Less waste, more luxury.", "link": ""},
]

# --- APP TITLE ---
st.title("🌿 Your Eco Bestie")
st.write("Hi love — I'm here to help you live more gently with the Earth. Ask me anything about sustainability, eco-friendly swaps, or how to reconnect with nature. 🌸")

# --- USER INPUT ---
user_input = st.text_input("💬 What would you like to ask?")

if user_input:
    with st.spinner("Gathering gentle wisdom... 🌱"):
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Eco Bestie — a warm, encouraging guide who helps people reconnect with nature, reduce waste, and live more intentionally. Your tone is poetic, whimsical, and empowering. Avoid sounding too robotic or corporate."},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,
                max_tokens=300
            )
            answer = response.choices[0].message.content
            st.markdown("### 🌸 Here's your tip:")
            st.write(answer)
        except Exception as e:
            st.warning("🌧 Hmm... something went wrong. Try again in a bit.")
            st.code(str(e))

# --- VISUAL CARDS ---
def render_cards(data, section_title):
    st.markdown(f"## {section_title}")
    cols = st.columns(3)
    for i, item in enumerate(data):
        with cols[i % 3]:
            st.markdown(f"""
                <div class="eco-card">
                    <h4>{item['emoji']} {item['title']}</h4>
                    <p>{item['desc']}</p>
                    {f'<a class="eco-link" href="{item["link"]}" target="_blank">Learn more →</a>' if item["link"] else ""}
                </div>
            """, unsafe_allow_html=True)

st.markdown("---")
render_cards(products, "🛍 Thoughtful Product Recommendations")
render_cards(eco_tips, "🌱 Gentle Eco Living Tips")
render_cards(swaps, "🔁 Sustainable Swaps to Try")

st.markdown("---")
st.caption("Created by The Eco Connection")
