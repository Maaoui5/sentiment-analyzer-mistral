# backend/main.py
from fastapi import FastAPI, Form, HTTPException
import requests

app = FastAPI()
OLLAMA_URL = "http://localhost:11434/api/generate"

@app.post("/analyze/")
def analyze_sentiment(text: str = Form(...)):
    prompt = (
        "Classify the sentiment of the following text as one of: Positive, Negative, Neutral.\n\n"
        f"Text:\n{text}\n\nRespond with a single word: Positive, Negative, or Neutral. "
        "Then, optionally add a one-sentence explanation."
    )
    payload = {"model": "mistral:latest", "prompt": prompt, "stream": False}
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=30)
        r.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error contacting Ollama: {e}")
    data = r.json()
    sentiment = (data.get("response") or data.get("output") or data.get("choices", [{}])[0].get("text"))
    if not sentiment:
        raise HTTPException(status_code=500, detail=f"Unexpected Ollama response: {data}")
    return {"sentiment": sentiment.strip()}
