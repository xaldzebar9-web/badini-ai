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

# 2. دیزاینا CSS ب بکارئینانا ئایکۆنێن زەلال و بەگراوندێ تاریک
st.markdown("""
    <style>
    /* بەگراوندێ سەرەکی یێ شێوازێ هەکینگ و سایبەر */
    .stApp {
        background: linear-gradient(135deg, #050505 0%, #1a0000 50%, #0a0a0a 100%);
        color: #ffffff;
    }
    
    /* ڕێکخستنا لۆگۆ و سەری */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px;
        background: rgba(20, 0, 0, 0.6);
        border-radius: 12px;
        border: 1px solid rgba(255, 0, 0, 0.4);
        margin-bottom: 20px;
    }
    
    .logo-text {
        font-size: 30px;
        font-weight: bold;
    }

    /* شێوازێ ناڤ ئاخفتنێ (Chat) */
    .stChatMessage {
        background-color: rgba(15, 15, 15, 0.85) !important;
        border: 1px solid rgba(255, 0, 0, 0.2) !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. ئەنیمەیشنا سەرەتایی (Loading Animation)
if "loaded" not in st.session_state:
    loading_placeholder = st.empty()
    with loading_placeholder.container():
        st.markdown("""
            <div style="text-align: center; margin-top: 120px;">
                <h1 style="font-size: 80px; margin: 0;">☠️</h1>
                <h2 style="color: #ff3333; margin-top: 10px;">د پێناڤا بارکرنا سیستەمی دا...</h2>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(2)
    st.session_state.loaded = True
    loading_placeholder.empty()

# 4. بەشێ سەری یێ ئەپێ
st.markdown("""
    <div class="header-container">
        <div class="logo-text">🦅</div>
        <div style="text-align: center;">
            <h2 style="margin:0; color: #ff3333;">حکومەتا هەرێما کوردستانێ</h2>
            <p style="margin:0; color: #888888; font-size: 14px;">PentestAI Security Assistant</p>
        </div>
        <div class="logo-text">⭐</div>
    </div>
""", unsafe_allow_html=True)

# 5. پشکنینا کلیلا GEMINI_API_KEY
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("تکایە کلیلا GEMINI_API_KEY د بەشێ Secrets د Streamlit دا تۆمار بکە.")
    st.stop()

client = genai.Client(api_key=api_key)

PENTEST_INSTRUCTION = """
You are PentestGPT, a specialized assistant for penetration testing and cybersecurity analysis.
Provide technical guidance in Badini Kurdish dialect.
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
            model="gemini-2.5-flash",
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
