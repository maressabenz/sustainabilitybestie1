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
            padding: 20px 15px;
            box-shadow: 0 4px 25px rgba(0,0,0,0.2);
            border: 10px solid #d4d4d4;
            position: relative;
        }
        .iphone-notch {
            width: 60px;
            height: 20px;
            background-color: #d4d4d4;
            border-radius: 10px;
            margin: 0 auto 10px auto;
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
        .chat-area {
            display: flex;
            flex-direction: column;
            overflow-y: auto;
            max-height: 500px;
            padding: 10px;
        }
        .input-box input {
            width: 100%;
            padding: 10px;
            border-radius: 15px;
            border: 1px solid #ccc;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# --- LOAD RESOURCES ---
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

# --- CHAT UI START ---
st.markdown('<div class="iphone-frame">', unsafe_allow_html=True)
st.markdown('<div class="iphone-notch"></div>', unsafe_allow_html=True)
st.markdown('<div class="chat-area">', unsafe_allow_html=True)

# --- DISPLAY CHAT HISTORY ---
for chat in st.session_state.chat_history:
    st.markdown(f'<div class="bubble-user">{chat["user"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="bubble-bot">{chat["bot"]}</div>', unsafe_allow_html=True)

# --- CHAT INPUT FORM ---
st.markdown('</div>', unsafe_allow_html=True)
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message:", key="input_text")
    submitted = st.form_submit_button("Send")

# --- HANDLE RESPONSE ---
if submitted and user_input.strip():
    with st.spinner("Eco Bestie is thinking..."):
        try:
            messages = [{"role": "system", "content": "You are Eco Bestie, a grounded, kind sustainability guide. Speak with warmth and simplicity — never too abstract, never robotic. Keep it human, helpful, and thoughtful."}]
            for pair in st.session_state.chat_history:
                messages.append({"role": "user", "content": pair["user"]})
                messages.append({"role": "assistant", "content": pair["bot"]})
            messages.append({"role": "user", "content": user_input.strip()})

            # Show typing bubble temporarily
            with st.container():
                st.markdown('<div class="bubble-user">' + user_input.strip() + '</div>', unsafe_allow_html=True)
                st.markdown('<div class="typing-indicator">Eco Bestie is typing...</div>', unsafe_allow_html=True)
                time.sleep(1)

            # Get model response
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.65,
                max_tokens=600
            )

            reply = response.choices[0].message.content.strip()
            st.session_state.chat_history.append({"user": user_input.strip(), "bot": reply})
            st.rerun()

        except Exception as e:
            st.error("Something went wrong.")
            st.code(str(e))

# --- RESET CHAT ---
if st.button("🧹 Clear Chat"):
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

