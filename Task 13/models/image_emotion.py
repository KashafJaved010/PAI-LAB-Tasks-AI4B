import cv2
from deepface import DeepFace
import os

# Load face cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_image_emotion(image_path):
    try:
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            return "No Image", 0.0

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

        if len(faces) == 0:
            return "Face Not Detected", 0.0

        # Analyze each face
        emotions = []
        confidences = []
        for i, (x, y, w, h) in enumerate(faces):
            face_roi = img[y:y+h, x:x+w]
            if face_roi.size == 0:
                continue
            # Resize for faster processing
            small_face = cv2.resize(face_roi, (48, 48))
            result = DeepFace.analyze(small_face, actions=['emotion'], enforce_detection=False, detector_backend='skip')
            emotion = result[0]['dominant_emotion']
            confidence = result[0]['emotion'][emotion] / 100.0
            emotions.append(f"Face{i+1}:{emotion}")
            confidences.append(confidence)

        # Combine results into a readable string
        if len(emotions) == 1:
            return emotions[0], confidences[0]
        else:
            combined_emotion = " | ".join(emotions)
            avg_confidence = sum(confidences) / len(confidences)
            return combined_emotion, avg_confidence

    except Exception as e:
        print("Image Emotion Error:", e)
        return "Face Not Detected", 0.0
