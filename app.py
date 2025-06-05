
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
# --- CHAT MEMORY SETUP ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("### 💬 Your Conversation with Eco Bestie")

# Display chat history
for msg in st.session_state.chat_history:
    st.markdown(f"**You:** {msg['user']}")
    st.markdown(f"**Eco Bestie:** {msg['bot']}")

# Input field
user_input = st.text_input(
    "Ask me something new 🌿",
    placeholder="e.g. What are eco-friendly alternatives to paper towels?"
)

# Process new input
if user_input:
    with st.spinner("Thinking green thoughts... 🌱"):
        try:
            # Build message history
            messages = [{"role": "system", "content": "You are Eco Bestie, a kind, grounded, and approachable sustainability guide. Be warm, helpful, and never too formal."}]
            for pair in st.session_state.chat_history:
                messages.append({"role": "user", "content": pair["user"]})
                messages.append({"role": "assistant", "content": pair["bot"]})
            messages.append({"role": "user", "content": user_input})

            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.65,
                max_tokens=600
            )

            reply = response.choices[0].message.content.strip()

            # Store in session
            st.session_state.chat_history.append({"user": user_input, "bot": reply})

            # Show new messages
            st.markdown(f"**You:** {user_input}")
            st.markdown(f"**Eco Bestie:** {reply}")

        except Exception as e:
            st.error("Oops! Something went wrong.")
            st.code(str(e))

# Optional: reset button
if st.button("🧹 Start over"):
    st.session_state.chat_history = []


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


