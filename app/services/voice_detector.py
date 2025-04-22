import speech_recognition as sr
from app.services.ai_mood_analysis import analyze_text_mood

def detect_mood_from_audio(file):
    recognizer = sr.Recognizer()

    with sr.AudioFile(file.file) as source:
        audio = recognizer.record(source)

    try:
        transcript = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        transcript = ""
    except sr.RequestError:
        transcript = ""

    mood_result = analyze_text_mood(transcript)

    return {
        "transcript": transcript,
        "emotion": mood_result["emotion"],
        "confidence": mood_result["confidence"],
        "original_label": mood_result["original_label"]
    }
