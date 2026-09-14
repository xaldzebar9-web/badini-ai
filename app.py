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

# بەستەرێن وێنەیان ژ سێرڤەرێن باوەڕپێکراو
KRG_LOGO = "https://raw.githubusercontent.com/wikipedia/commons/d/d4/Kurdistan_Regional_Government_Coat_of_arms.svg"
CT_LOGO = "https://upload.wikimedia.org/wikipedia/commons/5/50/CTU_Kurdistan.jpg"

# 2. دیزاینا بەگراوند و ڕوویێ ئەپێ ب CSS یێ پێشکەوتی
st.markdown(f"""
    <style>
    /* بەگراوندێ ڕەبتا تۆڕا تاریک و سوور */
    .stApp {{
        background-color: #0d0202;
        background-image: 
            radial-gradient(at 50% 0%, rgba(180, 0, 0, 0.35) 0px, transparent 75%),
            radial-gradient(at 100% 100%, rgba(100, 0, 0, 0.3) 0px, transparent 50%),
            radial-gradient(at 0% 100%, rgba(150, 0, 0, 0.2) 0px, transparent 50%);
        background-attachment: fixed;
        color: #ffffff;
    }}
    
    /* ڕێکخستنا هێدرێ سەری */
    .custom-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(18, 5, 5, 0.85);
        padding: 15px 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 30, 30, 0.4);
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.2);
        margin-bottom: 25px;
    }}
    
    .header-center {{
        text-align: center;
        flex-grow: 1;
    }}
    
    .krg-img {{
        height: 60px;
        margin-bottom: 5px;
    }}

    .ct-img {{
        height: 65px;
        border-radius: 8px;
        border: 1px solid rgba(255, 0, 0, 0.5);
    }}

    /* شێوازێ دیزاینا نامەیان */
    .stChatMessage {{
        background-color: rgba(20, 8, 8, 0.9) !important;
        border: 1px solid rgba(255, 0, 0, 0.25) !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }}
    </style>
""", unsafe_allow_html=True)

# 3. ئەنیمەیشنا سەرەتایی (Skull Animation)
if "loaded" not in st.session_state:
    loading_placeholder = st.empty()
    with loading_placeholder.container():
        st.markdown("""
            <div style="text-align: center; margin-top: 120px;">
                <div style="font-size: 90px; filter: drop-shadow(0 0 15px red);">☠️</div>
                <h2 style="color: #ff3333; font-family: monospace; margin-top: 15px;">د پێناڤا بارکرنا سیستەمی دا...</h2>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(2)
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
            <strong style="color: #ffb700; font-size: 20px;">حکومەتا هەرێما کوردستانێ</strong>
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
