from transformers import pipeline
import re

# Load sentiment model
nlp_pipe = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", framework="pt")

def clean_text(text: str):
    # Basic text cleaning (remove special characters, normalize whitespace)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def analyze_text_mood(text: str):
    cleaned_text = clean_text(text)

    # Run BERT sentiment analysis
    result = nlp_pipe(cleaned_text)[0]
    label = result["label"]
    score = result["score"]

    # Map BERT label to emotion
    if label == "POSITIVE":
        emotion = "motivated"
    elif label == "NEGATIVE":
        emotion = "stressed"
    else:
        emotion = "neutral"

    return {
        "emotion": emotion,
        "confidence": round(score, 2),
        "original_label": label
    }
