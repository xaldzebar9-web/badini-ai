import streamlit as st
from transformers import pipeline

st.title("ئەپا بادینی یا AI")

@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

classifier = load_model()

text = st.text_area("دەقەکێ بنڤێسە:")
if st.button("شیکار بکە"):
    if text:
        result = classifier(text)
        st.write(f"ئەنجام: {result[0]['label']} (دڵنیایی: %{round(result[0]['score']*100, 2)})")
