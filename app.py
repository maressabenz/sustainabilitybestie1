import streamlit as st
from openai import OpenAI

# Page configuration
st.set_page_config(page_title="Eco Bestie 🌿", layout="centered")

# Apply custom CSS
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

# Title and welcome message
st.title("🌿 Your Eco Bestie")
st.write("Ask anything about sustainable living, low-waste habits, or eco-friendly swaps. You can also explore some of my favorite product recommendations, eco tips, and sustainable swaps.")

# Static lists
product_recs = [
    "🌸 Shampoo Bar from Ethique — plastic-free and long-lasting",
    "🧴 Refillable glass hand soap from Blueland",
    "🛍 Organic cotton produce bags for grocery trips",
    "🕯 Coconut wax candles (non-toxic and biodegradable)",
    "🌱 Grow-your-own herb kits for windowsills",
    "🧼 Compostable dish scrubbers from ZeroWasteStore",
    "🚿 Water-saving shower head with filter (Hydraloop or Nebia)",
    "🧺 Wool dryer balls instead of single-use sheets",
    "☕ Reusable silicone coffee cup (Stojo or Huskee)",
    "💧 Filtered glass water bottle (like Soma or Kablo)"
]

eco_tips = [
    "🌿 Start your morning with a walk in nature — tech-free.",
    "🍃 Keep a zero-waste kit in your bag (utensils, straw, napkin).",
    "🧼 DIY your own all-purpose cleaner with vinegar and citrus peels.",
    "🌎 Choose secondhand or vintage whenever possible.",
    "🧺 Wash clothes on cold and line-dry when you can.",
    "🍋 Repurpose citrus rinds for cleaners or infusions.",
    "🛒 Support local farmers markets for seasonal produce.",
    "📦 Reuse packaging for storage or gifting.",
    "🔋 Unplug electronics when not in use — phantom energy adds up.",
    "🌸 Choose slow, natural rituals that align with your body and cycles."
]

swap_ideas = [
    "🧴 Swap plastic shampoo bottles for solid shampoo bars.",
    "🛍 Replace plastic bags with reusable produce & tote bags.",
    "🧽 Use compostable dishcloths instead of paper towels.",
    "💡 Switch to LED bulbs to save energy.",
    "🥤 Replace plastic straws with bamboo or stainless steel.",
    "📔 Use a digital planner or refillable notebooks.",
    "🎁 Wrap gifts in fabric or old maps instead of paper.",
    "🚿 Use soap bars instead of bottled body wash.",
    "🥣 Choose bulk goods over packaged whenever you can.",
    "🛒 Bring containers to refill stores for pantry items or cleaners."
]

# User input
user_input = st.text_input("💬 What would you like to ask?")

# Handle OpenAI response
if user_input:
    with st.spinner("Thinking green thoughts... 🌱"):
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You're a kind, empowering sustainability coach who offers practical advice about green living, eco swaps, nature reconnection, thoughtful consumption, and gentle habits. Keep answers friendly, concise, and brand-aligned."},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,
                max_tokens=300
            )
            answer = response.choices[0].message.content
            st.markdown("### 🌸 Here's your tip:")
            st.write(answer)
        except Exception as e:
            st.warning("🚫 Something went wrong. Please wait a moment and try again 🌿")
            st.code(str(e))

# Divider section
st.markdown("---")

# Expandable sections
with st.expander("🛍 10 Product Recommendations"):
    for item in product_recs:
        st.write(item)

with st.expander("🌱 10 Eco Living Tips"):
    for tip in eco_tips:
        st.write(tip)

with st.expander("🔁 10 Sustainable Swap Ideas"):
    for swap in swap_ideas:
        st.write(swap)

# Footer
st.markdown("---")
st.caption("Created with 🌿 by The Eco Connection | Powered by Streamlit & OpenAI")

