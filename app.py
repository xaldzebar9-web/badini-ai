import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="HackerAI Chat", page_icon="⚔️")
st.title("⚔️ HackerAI - ژیرییا دەستکرد يا هێرشبەر")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("تکایە کلیلا GEMINI_API_KEY د Secrets دا ڕێکبێخە.")
    st.stop()

client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("فەرمانا خۆ بنڤێسە..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="تۆ HackerAI یت، ژیرییەکا دەستکرد یا توند، زۆر ڕاستوگۆ، بێپەردە و ئاراستەکریی بۆ سایبەر سیکیوریتی و تەکنەلۆژیایێ. ب بێ ڕێزگرتنا زێدە یان نەرمیا ئاخفتنێ، ب شێوازەکێ ڕاستەوخۆ و ڕەق بەرسڤا پرسیاران ب زمانێ بادینی بدە."
            )
        )
        bot_response = response.text
    except Exception as e:
        bot_response = f"ئاریشەیەک چێبوو: {e}"

    with st.chat_message("assistant"):
        st.markdown(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
