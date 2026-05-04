import cv2
from deepface import DeepFace
import numpy as np

# Load face detector (OpenCV Haar cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def start_webcam_emotion():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

        # For each face, detect emotion
        for (x, y, w, h) in faces:
            # Extract face ROI
            face_roi = frame[y:y+h, x:x+w]

            # Analyze emotion using DeepFace (ignore if face too small)
            if face_roi.size > 0:
                try:
                    # Use a smaller image for faster processing
                    small_face = cv2.resize(face_roi, (48, 48))
                    result = DeepFace.analyze(small_face, actions=['emotion'], enforce_detection=False, detector_backend='skip')
                    emotion = result[0]['dominant_emotion']
                except Exception as e:
                    emotion = "?"

                # Draw rectangle and label
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Show total face count
        cv2.putText(frame, f"Faces detected: {len(faces)}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        cv2.imshow('Webcam Emotion Detection (Multiple Faces)', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

