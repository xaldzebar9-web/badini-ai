import streamlit as st

st.set_page_config(page_title="Badini AI Chat", page_icon="🤖")

st.title("🤖 چاتبۆتێ ژیرییا دەستکرد یا بادینی")
st.write("سڵاڤ! ئەز چاتبۆتێ تە مە. چ پرسیارەک یان ئاخفتنەک تە هەبێت بنڤێسە:")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("ل ێرە نڤێسینا خۆ بنڤێسە..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    bot_response = f"سوپاس بۆ پەیاما تە! تە گۆت: '{prompt}'. ئەز ل ێرەمە دا هاوکارییا تە بکەم."
    
    with st.chat_message("assistant"):
        st.markdown(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
