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
‏CT_LOGO = "https://upload.wikimedia.org/wikipedia/commons/5/50/CTU_Kurdistan.jpg"
# 2. دیزاینا بەگراوندێ ڕەنگێ تاریک و تۆڕا هەکینگێ (PentestGPT Grid Style)
st.markdown("""
    <style>
    /* بەگراوندێ سەرەکی ب شێوازێ PentestGPT Grid Pattern */
    .stApp {
        background-color: #080808;
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.05) 1px, transparent 1px);
        background-size: 30px 30px;
        color: #ffffff;
        font-family: 'Courier New', Courier, monospace;
    }

    /* ڕێکخستنا سەر دگەل لۆگۆیێ ڕاستەقینە یێ SVG */
    .custom-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(15, 15, 15, 0.9);
        padding: 15px 25px;
        border-radius: 12px;
        border: 1px solid rgba(0, 255, 65, 0.2);
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.1);
        margin-bottom: 25px;
    }

    .header-title {
        color: #00ff41;
        font-weight: bold;
        font-size: 22px;
        text-shadow: 0 0 8px rgba(0, 255, 65, 0.4);
        margin: 0;
        text-align: center;
    }

    /* شێوازێ دیزاینا چاتێ */
    .stChatMessage {
        background-color: rgba(18, 18, 18, 0.95) !important;
        border: 1px solid rgba(0, 255, 65, 0.15) !important;
        border-radius: 10px !important;
    }
    
    /* شێوازێ بەشێ نڤێسینێ */
    .stChatInput {
        border-color: rgba(0, 255, 65, 0.3) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. ئەنیمەیشنا سەرەتایی (Skull Animation) بۆ ماوەی ٧ سانیان
if "loaded" not in st.session_state:
    loading_placeholder = st.empty()
    with loading_placeholder.container():
        st.markdown("""
            <div style="text-align: center; margin-top: 120px;">
                <div style="font-size: 100px; filter: drop-shadow(0 0 20px #00ff41); margin-bottom: 10px;">☠️</div>
                <h2 style="color: #00ff41; font-family: monospace;">SYSTEM INITIALIZING...</h2>
                <p style="color: #888888;">د پێناڤا بارکرنا سیستەمی دا (7 Seconds)...</p>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(7)
    st.session_state.loaded = True
    loading_placeholder.empty()

# 4. بەشێ سەری (Header دگەل ئایکۆنێن ب بێ بەگراوند)
st.markdown("""
    <div class="custom-header">
        <div style="font-size: 35px; filter: drop-shadow(0 0 5px #00ff41);">🦅</div>
        <div>
            <h2 class="header-title">&lt; PENTEST_GPT Kurdish /&gt;</h2>
            <div style="text-align: center; color: #888888; font-size: 12px; margin-top: 4px;">حکومەتا هەرێما کوردستانێ</div>
        </div>
        <div style="font-size: 35px; filter: drop-shadow(0 0 5px #00ff41);">🛡️</div>
    </div>
""", unsafe_allow_html=True)

# 5. گرێدانا Gemini API
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("تکایە کلیلا GEMINI_API_KEY د بەشێ Secrets دا تۆمار بکە.")
    st.stop()

client = genai.Client(api_key=api_key)

PENTEST_INSTRUCTION = """
You are PentestGPT, a specialized cybersecurity and penetration testing assistant.
Provide technical responses in Badini Kurdish dialect.
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
