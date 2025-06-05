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
        .chat-bubble-user {
            background-color: #ffffff;
            color: #2f2e2d;
            border-radius: 18px;
            padding: 10px 15px;
            margin: 5px 0;
            max-width: 60%;
            align-self: flex-end;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .chat-bubble-bot {
            background-color: #d6e8c5;
            color: #2f2e2d;
            border-radius: 18px;
            padding: 10px 15px;
            margin: 5px 0;
            max-width: 60%;
            align-self: flex-start;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .chat-container {
            display: flex;
            flex-direction: column;
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

# --- TITLE & MEMORY SETUP ---
st.title("Hi! I'm your Eco Bestie 🌿")
st.write("I'm here to help you live more gently with the Earth. Ask me anything about sustainability, eco-friendly swaps, or how to reconnect with nature. 🌸")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.text_input(
    "Type your question",
    key="user_input",
    placeholder="e.g. What are some low-waste bathroom swaps?"
)

# --- CHAT HEADER ---
st.markdown("### 🌿 Chat with Eco Bestie")

# --- DISPLAY CHAT HISTORY ---
chat_html = '<div class="chat-container">'
for pair in st.session_state.chat_history:
    chat_html += f'<div class="chat-bubble-user"><b>You:</b> {pair["user"]}</div>'
    chat_html += f'<div class="chat-bubble-bot"><b>Eco Bestie:</b> {pair["bot"]}</div>'
chat_html += '</div>'
st.markdown(chat_html, unsafe_allow_html=True)

# --- HANDLE USER INPUT ---
if st.session_state.user_input:
    with st.spinner("Eco Bestie is thinking... 🌱"):
        try:
            messages = [{"role": "system", "content": "You are Eco Bestie, a grounded, practical, and kind sustainability guide who speaks like a thoughtful friend. Avoid fantasy language. Keep it real, relatable, and warm."}]
            for pair in st.session_state.chat_history:
                messages.append({"role": "user", "content": pair["user"]})
                messages.append({"role": "assistant", "content": pair["bot"]})
            messages.append({"role": "user", "content": st.session_state.user_input})

            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.65,
                max_tokens=600
            )

            reply = response.choices[0].message.content.strip()
            st.session_state.chat_history.append({"user": st.session_state.user_input, "bot": reply})
            st.session_state.user_input = ""  # 🛑 prevent re-loop
            st.rerun()

        except Exception as e:
            st.error("Oops! Something went wrong.")
            st.code(str(e))

# --- RESET CHAT BUTTON ---
if st.button("🧹 Start Over"):
    st.session_state.chat_history = []
    st.session_state.user_input = ""
    st.rerun()

# --- DISPLAY CARDS ---
def render_cards(data, section_title):
    st.markdown(f"## {section_title}")
    cols = st.columns(3)
    for i, item in enumerate(data):
        with cols[i % 3]:
            image_url = item.get("image", "")
            image_link = item.get("image_link", item.get("link", ""))
            img_html = (
                f'<a href="{image_link}" target="_blank">'
                f'<img src="{image_url}" style="width:100%; border-radius:12px; margin-bottom:0.5rem;" />'
                f'</a>'
            ) if image_url else ""

            st.markdown(f"""
                <div style="background-color:#fff; padding:1rem; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.08); text-align:center;">
                    {img_html}
                    <h4>{item['emoji']} {item['title']}</h4>
                    <p>{item['desc']}</p>
                    <a href="{item['link']}" target="_blank" style="color:#4a7c59; font-weight:500;">Learn more →</a>
                </div>
            """, unsafe_allow_html=True)

# --- RENDER RESOURCE SECTIONS ---
st.markdown("---")
render_cards(products, "🛍 Thoughtful Product Recommendations")
render_cards(eco_tips, "🌱 Gentle Eco Living Tips")
render_cards(swaps, "🔁 Sustainable Swaps to Try")
st.markdown("---")
st.caption("Created by Maressa Benz | The Eco Connection")

