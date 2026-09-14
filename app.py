import time
import streamlit as st
from google import genai
from google.genai import types

# 1. ڕێکخستنا سەرەکی یا لاپەڕەی
st.set_page_config(
    page_title="PentestAI Assistant",
    page_icon="🛡️",
    layout="wide"
)

KRG_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Kurdistan_Regional_Government_Coat_of_arms.svg/1200px-Kurdistan_Regional_Government_Coat_of_arms.svg.png"
CT_LOGO = "https://upload.wikimedia.org/wikipedia/commons/5/50/CTU_Kurdistan.jpg"
SKULL_GIF = "https://i.pinimg.com/originals/30/ca/87/30ca877eb4bd1e5c3e7e22df72120464.gif"

# 2. دیزاینا بەگراوندێ لڤلڤۆک و پاککرنا بەگراوندێ سپی یێ لۆگۆیان ب CSS
st.markdown(f"""
    <style>
    /* بەگراوندێ سەرەکی یێ لڤلڤۆک (Animated Gradient + Binary Effect) */
    .stApp {{
        background: linear-gradient(-45deg, #0a0000, #2b0000, #150000, #000000);
        background-size: 400% 400%;
        animation: gradientBG 10s ease infinite;
        color: #ffffff;
    }}

    @keyframes gradientBG {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    /* ڕێکخستنا هێدرێ سەری */
    .custom-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(10, 0, 0, 0.65);
        padding: 12px 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 0, 0, 0.4);
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.3);
        margin-bottom: 20px;
    }}
    
    .header-center {{
        text-align: center;
        flex-grow: 1;
    }}
    
    /* لۆگۆیا حکومەتێ ب بێ بەگراوند */
    .krg-img {{
        height: 65px;
        background: transparent;
        mix-blend-mode: screen; /* لادانا سپیاتیێ */
    }}

    /* لۆگۆیا دژەتیرۆر ب بێ بەگراوندی سپی */
    .ct-img {{
        height: 65px;
        border-radius: 50%;
        mix-blend-mode: lighten; /* لادانا سپیاتیێ د لۆگۆیێ دا */
        background: transparent;
    }}

    /* شێوازێ دیزاینا چاتێ */
    .stChatMessage {{
        background-color: rgba(15, 5, 5, 0.85) !important;
        border: 1px solid rgba(255, 0, 0, 0.25) !important;
        border-radius: 12px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 3. ئەنیمەیشنا سەرەتایی (Skull Animation)
if "loaded" not in st.session_state:
    loading_placeholder = st.empty()
    with loading_placeholder.container():
        st.markdown(f"""
            <div style="text-align: center; margin-top: 100px;">
                <img src="{SKULL_GIF}" width="250" style="border-radius: 15px; mix-blend-mode: lighten;">
                <h2 style="color: #ff3333; font-family: monospace; margin-top: 15px;">د پێناڤا بارکرنا سیستەمی دا...</h2>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(2.5)
    st.session_state.loaded = True
    loading_placeholder.empty()

# 4. بەشێ سەری (Header)
st.markdown(f"""
    <div class="custom-header">
        <div>
            <img src="{CT_LOGO}" class="ct-img" alt="CT Unit">
        </div>
        <div class="header-center">
            <img src="{KRG_LOGO}" class="krg-img" alt="KRG Logo"><br>
            <strong style="color: #ffb700; font-size: 18px;">حکومەتا هەرێما کوردستانێ</strong>
        </div>
        <div style="width: 65px;"></div>
    </div>
""", unsafe_allow_html=True)

st.title("🛡️ PentestAI Assistant")

# 5. گرێدانا Gemini API
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("تکایە کلیلا GEMINI_API_KEY د بەشێ Secrets دا تۆمار بکە.")
    st.stop()

client = genai.Client(api_key=api_key)

PENTEST_INSTRUCTION = """
You are PentestGPT, a specialized cybersecurity and penetration testing assistant.
Provide clear technical responses in Badini Kurdish dialect.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("فەرمان یان پرسیارەکێ بنڤێسە..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=PENTEST_INSTRUCTION
            )
        )
        bot_response = response.text
    except Exception as e:
        bot_response = f"ئاریشە: {e}"

    with st.chat_message("assistant"):
        st.markdown(bot_response)

    st.session_state.messages.append({"role": "assistant", "content": bot_response})
