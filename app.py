import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="PentestGPT Assistant", page_icon="🛡️")
st.title("🛡️ PentestGPT Assistant")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("تکایە کلیلا GEMINI_API_KEY د بەشێ Secrets د Streamlit دا تۆمار بکە.")
    st.stop()

client = genai.Client(api_key=api_key)

# دەستوور و پرۆمپتێ سەرەکی یێ PentestGPT
PENTEST_INSTRUCTION = """
You are PentestGPT, an autonomous cybersecurity and penetration testing assistant.
Your goal is to guide security researchers through vulnerability analysis, system evaluation, and ethical penetration testing.
Follow a structured flow: Reconnaissance -> Vulnerability Scanning -> Exploitation Assessment -> Mitigation.
Always respond in Badini Kurdish dialect with accurate, direct, and technical explanations.
Do not act as a general chatbot; strictly maintain your persona as an expert ethical hacking terminal tool.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("فەرمان یان پرسیارەکێ د بوارێ ئاسایشێ دا بنڤێسە..."):
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
