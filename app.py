import streamlit as st
import pandas as pd
from openai import OpenAI
import time

# --- CONFIG & STYLE ---
st.set_page_config(page_title="Eco Bestie by The Eco Connection🌿", layout="centered")

st.markdown("""
    <style>
        html, body {
            background-color: #ecebe4;
        }
        .iphone-frame {
            max-width: 400px;
            margin: 0 auto;
            background: #fdfdfb;
            border-radius: 40px;
            padding: 15px 10px 60px 10px;
            box-shadow: 0 4px 25px rgba(0,0,0,0.15);
            border: 10px solid #d4d4d4;
            position: relative;
            height: 700px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .iphone-notch {
            width: 60px;
            height: 20px;
            background-color: #d4d4d4;
            border-radius: 10px;
            margin: 0 auto 10px auto;
        }
        .chat-area {
            display: flex;
            flex-direction: column;
            overflow-y: scroll;
            flex-grow: 1;
            padding: 10px;
            scrollbar-width: thin;
        }
        .bubble-user {
            background-color: #bfeec2;
            color: #1b1b1b;
            border-radius: 18px;
            padding: 10px 14px;
            margin: 6px 0;
            max-width: 80%;
            align-self: flex-end;
            margin-left: auto;
        }
        .bubble-bot {
            background-color: #e6e6eb;
            color: #1b1b1b;
            border-radius: 18px;
            padding: 10px 14px;
            margin: 6px 0;
            max-width: 80%;
            align-self: flex-start;
        }
        .typing-indicator {
            background-color: #e6e6eb;
            color: #1b1b1b;
            border-radius: 18px;
            padding: 6px 12px;
            margin: 6px 0;
            max-width: 80%;
            align-self: flex-start;
            font-style: italic;
            opacity: 0.7;
        }
        .input-wrapper {
            position: absolute;
            bottom: 15px;
            left: 10px;
            right: 10px;
            display: flex;
            align-items: center;
        }
        .input-wrapper input {
            flex-grow: 1;
            border-radius: 999px;
            padding: 12px 50px 12px 15px;
            border: 1px solid #ccc;
            outline: none;
            font-size: 14px;
        }
        .send-button {
            position: absolute;
            right: 20px;
            background: none;
            border: none;
            color: #4a7c59;
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

# --- SESSION STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# --- IPHONE FRAME ---
st.markdown('<div class="iphone-frame">', unsafe_allow_html=True)
st.markdown('<div class="iphone-notch"></div>', unsafe_allow_html=True)
st.markdown('<div class="chat-area">', unsafe_allow_html=True)

# --- DISPLAY CHAT HISTORY ---
for chat in st.session_state.chat_history:
    st.markdown(f'<div class="bubble-user">{chat["user"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="bubble-bot">{chat["bot"]}</div>', unsafe_allow_html=True)

# --- CHAT FORM ---
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
form = st.form(key="chat_form", clear_on_submit=True)
col1, col2 = form.columns([5, 1])
user_input = col1.text_input("", placeholder="Send a message...", label_visibility="collapsed")
send_button = col2.form_submit_button("➤")
st.markdown('</div>', unsafe_allow_html=True)

# --- HANDLE SUBMISSION ---
if send_button and user_input.strip():
    with st.spinner("Eco Bestie is typing... 🌿"):
        try:
            messages = [{"role": "system", "content": "You are Eco Bestie, a kind, grounded sustainability guide who speaks in a warm, clear tone. No fantasy, just practical, emotionally intelligent guidance."}]
            for pair in st.session_state.chat_history:
                messages.append({"role": "user", "content": pair["user"]})
                messages.append({"role": "assistant", "content": pair["bot"]})
            messages.append({"role": "user", "content": user_input.strip()})

            # Temporary typing bubble
            st.session_state.chat_history.append({"user": user_input.strip(), "bot": "Eco Bestie is typing..."})
            st.rerun()

        except Exception as e:
            st.error("Something went wrong.")
            st.code(str(e))

# --- POST TYPING SIMULATION ---
if st.session_state.chat_history and st.session_state.chat_history[-1]["bot"] == "Eco Bestie is typing...":
    user_text = st.session_state.chat_history[-1]["user"]
    messages = [{"role": "system", "content": "You are Eco Bestie, a kind, grounded sustainability guide who speaks in a warm, clear tone. No fantasy, just practical, emotionally intelligent guidance."}]
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
    st.rerun()

# --- RESET CHAT ---
if st.button("🧹 Clear Chat"):
    st.session_state.chat_history = []

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

st.markdown("---")
render_cards(products, "🛍 Thoughtful Product Recommendations")
render_cards(eco_tips, "🌱 Gentle Eco Living Tips")
render_cards(swaps, "🔁 Sustainable Swaps to Try")
st.markdown("---")
st.caption("Created by Maressa Benz | The Eco Connection")
