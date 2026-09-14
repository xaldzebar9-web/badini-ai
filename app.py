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

# 2. بەستەرێن ڕاستەوخۆ یێن وێنەیان
KRG_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Kurdistan_Regional_Government_Coat_of_arms.svg/1200px-Kurdistan_Regional_Government_Coat_of_arms.svg.png"
CT_LOGO = "https://upload.wikimedia.org/wikipedia/commons/5/50/CTU_Kurdistan.jpg"
SKULL_IMG = "https://i.pinimg.com/originals/30/ca/87/30ca877eb4bd1e5c3e7e22df72120464.gif"
BG_NET_IMG = "https://i.pinimg.com/originals/60/0a/85/600a85012e84d436a5c2d6eb99a9a5f7.jpg"

# 3. دیزاینا بەگراوند و ڕوویێ ئەپێ ب CSS
st.markdown(f"""
    <style>
    .stApp {{
        background: url('{BG_NET_IMG}') no-repeat center center fixed;
        background-size: cover;
        color: #ffffff;
    }}
    
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.75);
        z-index: -1;
    }}

    .header-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 25px;
        background: rgba(15, 0, 0, 0.7);
        border-radius: 12px;
        border: 1px solid rgba(255, 0, 0, 0.4);
        margin-bottom: 25px;
    }}
    
    .header-logo {{
        height: 70px;
        object-fit: contain;
    }}

    .stChatMessage {{
        background-color: rgba(15, 15, 15, 0.88) !important;
        border: 1px solid rgba(255, 0, 0, 0.25) !important;
        border-radius: 10px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 4. ئەنیمەیشنا سەرەتایی یا لۆدینگێ (Skull Loading Animation)
if "loaded" not in st.session_state:
    loading_placeholder = st.empty()
    with loading_placeholder.container():
        st.markdown(f"""
            <div style="text-align: center; margin-top: 100px;">
                <img src="{SKULL_IMG}" width="240" style="border-radius: 10px;">
                <h3 style="color: #ff3333; margin-top: 15px;">د پێناڤا بارکرنا سیستەمی دا...</h3>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(3)
    st.session_state.loaded = True
    loading_placeholder.empty()

# 5. بەشێ سەری (Header دگەل لۆگۆیێ حکومەتێ د ناڤەڕاستێ دا و دژەتیرۆر د چەپێ دا)
st.markdown(f"""
    <div class="header-container">
        <img src="{CT_LOGO}" class="header-logo" alt="CT Unit">
        <div style="text-align: center;">
            <img src="{KRG_LOGO}" class="header-logo" alt="KRG Logo">
            <h3 style="margin: 5px 0 0 0; color: #ffaa00;">حکومەتا هەرێما کوردستانێ</h3>
        </div>
        <div style="width: 70px;"></div>
    </div>
""", unsafe_allow_html=True)

st.title("🛡️ PentestAI Assistant")

# 6. گرێدانا Gemini API ب مۆدێلا نوو
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
