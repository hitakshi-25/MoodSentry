from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

# Load tokenizer and model directly
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

def analyze_text_mood(text: str):
    # Tokenize input
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    # Predict logits
    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)

    # Get label and score
    label_id = torch.argmax(probs, dim=1).item()
    score = probs[0][label_id].item()
    label = model.config.id2label[label_id]

    # Map to emotion
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
