import streamlit as st
import pandas as pd
from openai import OpenAI

# --- CONFIG ---
st.set_page_config(page_title="Eco Bestie 🌿", layout="centered")

# --- STYLE ---
st.markdown("""
    <style>
        body {
            background-color: #f4f1ea;
            font-family: 'Georgia', serif;
        }
        .chat-container {
            max-width: 700px;
            margin: auto;
            padding: 1rem;
        }
        .user-bubble {
            background-color: #d8f3dc;
            color: #1b1b1b;
            border-radius: 20px;
            padding: 12px 16px;
            margin: 8px 0;
            max-width: 75%;
            align-self: flex-end;
        }
        .bot-bubble {
            background-color: #fff;
            color: #2f2e2d;
            border-radius: 20px;
            padding: 12px 16px;
            margin: 8px 0;
            max-width: 75%;
            align-self: flex-start;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }
        .chat-wrap {
            display: flex;
            flex-direction: column;
        }
        .input-bar {
            margin-top: 1rem;
            display: flex;
            gap: 10px;
        }
        .input-bar input {
            flex: 1;
            padding: 12px;
            border-radius: 999px;
            border: 1px solid #ccc;
            outline: none;
        }
        .send-button {
            padding: 10px 20px;
            border-radius: 999px;
            border: none;
            background-color: #40916c;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ9X4uUiJ62AowI-E41-Q3CfMP24rFpe6Amci5IdB7gWg8SBCZOX-q4B7J0zv2uXouNo5vBipwxSnKb/pub?output=csv"
    return pd.read_csv(sheet_url)

df = load_data()
products = df[df["type"] == "product"].to_dict(orient="records")
eco_tips = df[df["type"] == "eco_tip"].to_dict(orient="records")
swaps = df[df["type"] == "swap"].to_dict(orient="records")

# --- CHAT STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# --- MAIN APP LAYOUT ---
st.title("🌿 Eco Bestie")
st.write("Ask anything about sustainable living, conscious swaps, or gentle habits for the planet.")

st.markdown('<div class="chat-container"><div class="chat-wrap">', unsafe_allow_html=True)
for pair in st.session_state.chat_history:
    st.markdown(f'<div class="user-bubble">🧍‍♀️ {pair["user"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="bot-bubble">🌿 {pair["bot"]}</div>', unsafe_allow_html=True)
st.markdown('</div></div>', unsafe_allow_html=True)

# --- INPUT BAR ---
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    user_input = col1.text_input("Type your question", label_visibility="collapsed", placeholder="Type your question here...")
    submitted = col2.form_submit_button("Send")
    if submitted and user_input.strip():
        st.session_state.chat_history.append({"user": user_input.strip(), "bot": "Eco Bestie is thinking..."})
        st.session_state.user_input = user_input.strip()
        st.experimental_rerun()

# --- GET RESPONSE ---
if st.session_state.chat_history and st.session_state.chat_history[-1]["bot"] == "Eco Bestie is thinking...":
    user_text = st.session_state.chat_history[-1]["user"]
    messages = [{"role": "system", "content": "You are Eco Bestie, a practical, kind sustainability guide who speaks warmly and clearly."}]
    for pair in st.session_state.chat_history[:-1]:
        messages.append({"role": "user", "content": pair["user"]})
        messages.append({"role": "assistant", "content": pair["bot"]})
    messages.append({"role": "user", "content": user_text})

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.65,
        max_tokens=600
    )
    reply = response.choices[0].message.content.strip()
    st.session_state.chat_history[-1]["bot"] = reply
    st.experimental_rerun()

# --- RESET BUTTON ---
if st.button("🧹 Start Over"):
    st.session_state.chat_history = []

# --- RESOURCE CARDS ---
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

st.markdown("---")
render_cards(products, "🛍 Thoughtful Product Recommendations")
render_cards(eco_tips, "🌱 Gentle Eco Living Tips")
render_cards(swaps, "🔁 Sustainable Swaps to Try")
st.markdown("---")
st.caption("Created by Maressa Benz | The Eco Connection")
