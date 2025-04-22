import cv2
import numpy as np
from keras.models import load_model

# Load a compact emotion model (e.g., FER2013 pretrained)
emotion_model = load_model("models/emotion_model.h5")
emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

def detect_emotion_from_image(image_path: str):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi = gray[y:y+h, x:x+w]
        roi = cv2.resize(roi, (48, 48)) / 255.0
        roi = roi.reshape(1, 48, 48, 1)

        prediction = emotion_model.predict(roi)
        emotion = emotion_labels[np.argmax(prediction)]
        return emotion

    return "neutral"  # fallback if no face
