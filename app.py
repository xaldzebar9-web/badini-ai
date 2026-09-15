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

# 🔗 بەستەرێن وێنەیان (تە دشی لۆگۆیا نوو ل ڤێرێ دانێ)
NEW_LOGO = "https://raw.githubusercontent.com/wikipedia/commons/d/d4/Kurdistan_Regional_Government_Coat_of_arms.svg"
CT_LOGO = "https://upload.wikimedia.org/wikipedia/commons/5/50/CTU_Kurdistan.jpg"
SKULL_GIF = "https://i.pinimg.com/originals/30/ca/87/30ca877eb4bd1e5c3e7e22df72120464.gif"

# 2. دروستکرنا بەگراوندا لڤلڤۆک ب JavaScript (Matrix Digital Rain)
matrix_code = """
<style>
    body { margin: 0; overflow: hidden; background: black; }
    canvas { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1; }
</style>
<canvas id="matrix"></canvas>
<script>
    const canvas = document.getElementById('matrix');
    const ctx = canvas.getContext('2d');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const letters = '0110100101010101010101';
    const fontSize = 14;
    const columns = canvas.width / fontSize;
    const drops = Array(Math.floor(columns)).fill(1);

    function draw() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = '#ff1111';
        ctx.font = fontSize + 'px monospace';

        for (let i = 0; i < drops.length; i++) {
            const text = letters.charAt(Math.floor(Math.random() * letters.length));
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);

            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }
    setInterval(draw, 33);
</script>
"""
components.html(matrix_code, height=0)

# 3. دیزاینا CSS بۆ لۆگۆ و شاشێ
st.markdown(f"""
    <style>
    .stApp {{
        background: transparent;
        color: #ffffff;
    }}

    .custom-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(15, 0, 0, 0.85);
        padding: 12px 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 0, 0, 0.5);
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.4);
        margin-bottom: 20px;
    }}
    
    .header-center {{
        text-align: center;
        flex-grow: 1;
    }}
    
    .main-logo {{
        height: 70px;
        mix-blend-mode: lighten;
    }}

    .ct-img {{
        height: 65px;
        border-radius: 50%;
        mix-blend-mode: lighten;
    }}

    .stChatMessage {{
        background-color: rgba(15, 5, 5, 0.9) !important;
        border: 1px solid rgba(255, 0, 0, 0.3) !important;
        border-radius: 12px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 4. ئەنیمەیشنا سەرەتایی (Skull Animation) بۆ ماوەی ٧ چڵکان (7 Seconds)
if "loaded" not in st.session_state:
    loading_placeholder = st.empty()
    with loading_placeholder.container():
        st.markdown(f"""
            <div style="text-align: center; margin-top: 100px;">
                <img src="{SKULL_GIF}" width="250" style="mix-blend-mode: lighten; filter: drop-shadow(0 0 15px red);">
                <h2 style="color: #ff3333; font-family: monospace; margin-top: 15px;">د پێناڤا بارکرنا سیستەمی دا...</h2>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(7)  # ⏱️ ٧ سانیێن ڕاستەقینە
    st.session_state.loaded = True
    loading_placeholder.empty()

# 5. بەشێ سەری (Header دگەل لۆگۆیێ چەپێ و ناڤەڕاستێ)
st.markdown(f"""
    <div class="custom-header">
        <div>
            <img src="{CT_LOGO}" class="ct-img" alt="CT Unit">
        </div>
        <div class="header-center">
            <img src="{NEW_LOGO}" class="main-logo" alt="Main Logo">
        </div>
        <div style="width: 65px;"></div>
    </div>
""", unsafe_allow_html=True)

st.title("🛡️ PentestAI Assistant")

# 6. گرێدانا Gemini API
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
# دەنگێ ئۆتۆماتیکی ل دەمێ ڤەبوونا ئەپێ
st.components.v1.html("""
    <script>
        window.addEventListener('load', function() {
            var msg = new SpeechSynthesisUtterance("بەخێربێی بۆ ئاژانسی هەواڵگێری");
            msg.lang = "ckb"; // زاراڤەیێ کوردی / عەرەبی
            msg.rate = 0.9;  # خێرایییا دەنگی
            window.speechSynthesis.speak(msg);
        });
    </script>
""", height=0)
