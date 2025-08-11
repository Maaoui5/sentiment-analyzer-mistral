# frontend/app.py
import streamlit as st
import requests

st.title("Sentiment Analyzer (Mistral)")

text_input = st.text_area("Enter your sentence here:")

if st.button("Analyze"):
    if not text_input.strip():
        st.warning("Please enter text first.")
    else:
        with st.spinner("Analyzing..."):
            try:
                res = requests.post("http://localhost:8000/analyze/", data={"text": text_input}, timeout=20)
                res.raise_for_status()
                sentiment = res.json().get("sentiment", "Error")
                st.subheader("Predicted Sentiment:")
                st.write(sentiment)
            except Exception as e:
                st.error(f"Error: {e}")
