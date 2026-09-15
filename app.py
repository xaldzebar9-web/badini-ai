import time
import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types

# 1. ڕێکخستنا سەرەکی یا لاپەڕەی
st.set_page_config(
    page_title="PentestAI Assistant",
    page_icon="🛡️",
    layout="wide"
)

# 2. دیزاینا بەگراوندێ ڕەنگێ تاریک و تۆڕا هەکینگێ (Grid Style)
st.markdown("""
    <style>
    .stApp {
        background-color: #080808;
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.05) 1px, transparent 1px);
        background-size: 30px 30px;
        color: #ffffff;
        font-family: 'Courier New', Courier, monospace;
    }

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

    .stChatMessage {
        background-color: rgba(18, 18, 18, 0.95) !important;
        border: 1px solid rgba(0, 255, 65, 0.15) !important;
        border-radius: 10px !important;
    }
    
    .stButton > button {
        background-color: #ff1111 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: 1px solid #ff5555 !important;
        padding: 10px 25px !important;
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.5) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. بەشێ دەستپێکرن و لۆدینگێ ب دەنگ
if "system_started" not in st.session_state:
    st.session_state.system_started = False

if not st.session_state.system_started:
    st.markdown("""
        <div style="text-align: center; margin-top: 100px;">
            <div style="font-size: 90px; filter: drop-shadow(0 0 20px #ff0000); margin-bottom: 10px;">☠️</div>
            <h2 style="color: #ff3333; font-family: monospace;">سیستەم د ئامادەباشیێ دا یە</h2>
            <p style="color: #888888;">بۆ کارێنانی دەنگی و کارپێکرنا ئەپێ کلیک ل سەر دوگمەیا خوارێ بکە</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 دۆخێ دەستپێکرنا سیستەمی", use_container_width=True):
            # کارپێکرنا دەنگی ب ڕێکا Web Speech API
            components.html("""
                <script>
                    var msg = new SpeechSynthesisUtterance("بەخێربێی بۆ ئاژانسی هەواڵگێری");
                    msg.lang = "ckb";
                    msg.rate = 0.9;
                    window.speechSynthesis.speak(msg);
                </script>
            """, height=0)
            
            # نیشاندانا ڕاگەیاندنا لۆدینگێ بۆ ماوەی ٧ سانیان
            with st.spinner("د پێناڤا بارکرنا سیستەمی دا (7 Seconds)..."):
                time.sleep(7)
                
            st.session_state.system_started = True
            st.rerun()
    st.stop()

# 4. بەشێ سەری (Header)
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
            model="gemini-2.0-flash",
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
