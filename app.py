import streamlit as st
import pandas as pd
from openai import OpenAI

# --- CONFIG & STYLE ---
st.set_page_config(page_title="Eco Bestie by The Eco Connection🌿", layout="centered")

st.markdown("""
    <style>
        html, body {
            background-color: #ecebe4;
        }
        .iphone-shell {
            display: flex;
            justify-content: center;
        }
        .iphone-frame {
            max-width: 375px;
            width: 100%;
            height: 740px;
            background: #fdfdfb;
            border-radius: 40px;
            border: 10px solid #ccc;
            box-shadow: 0 4px 25px rgba(0,0,0,0.2);
            position: relative;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        .iphone-notch {
            width: 60px;
            height: 20px;
            background-color: #d4d4d4;
            border-radius: 10px;
            margin: 8px auto 4px auto;
        }
        .chat-area {
            flex-grow: 1;
            overflow-y: auto;
            padding: 12px;
            display: flex;
            flex-direction: column;
        }
        .bubble-user {
            background-color: #00c759;
            color: white;
            border-radius: 20px;
            padding: 10px 14px;
            margin: 6px 0;
            max-width: 75%;
            align-self: flex-end;
        }
        .bubble-bot {
            background-color: #e5e5ea;
            color: #1b1b1b;
            border-radius: 20px;
            padding: 10px 14px;
            margin: 6px 0;
            max-width: 75%;
            align-self: flex-start;
        }
        .input-bar {
            padding: 10px 12px;
            display: flex;
            gap: 10px;
            align-items: center;
            background-color: #f1f1f1;
            border-top: 1px solid #ccc;
        }
        .input-bar input {
            flex-grow: 1;
            border-radius: 999px;
            padding: 10px 16px;
            border: 1px solid #ccc;
            outline: none;
            font-size: 14px;
        }
        .send-button {
            background-color: #00c759;
            border: none;
            color: white;
            padding: 8px 16px;
            border-radius: 999px;
            font-size: 14px;
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

# --- LAYOUT: IPHONE SHELL ---
st.markdown('<div class="iphone-shell">', unsafe_allow_html=True)
st.markdown('<div class="iphone-frame">', unsafe_allow_html=True)
st.markdown('<div class="iphone-notch"></div>', unsafe_allow_html=True)

# --- CHAT AREA ---
st.markdown('<div class="chat-area">', unsafe_allow_html=True)
for chat in st.session_state.chat_history:
    st.markdown(f'<div class="bubble-user">{chat["user"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="bubble-bot">{chat["bot"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- INPUT BAR + FORM ---
with st.form("chat_form", clear_on_submit=True):
    st.markdown('<div class="input-bar">', unsafe_allow_html=True)
    col1, col2 = st.columns([5, 1])
    user_input = col1.text_input("Type your question here...", label_visibility="collapsed")
    send = col2.form_submit_button("Send", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# --- HANDLE CHAT SUBMISSION ---
if send and user_input.strip():
    st.session_state.chat_history.append({"user": user_input.strip(), "bot": "Eco Bestie is typing..."})
    st.rerun()

if st.session_state.chat_history and st.session_state.chat_history[-1]["bot"] == "Eco Bestie is typing...":
    user_text = st.session_state.chat_history[-1]["user"]
    messages = [{"role": "system", "content": "You are Eco Bestie, a practical, kind sustainability guide. Speak clearly and warmly like a grounded best friend."}]
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

# --- END FRAME ---
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

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
