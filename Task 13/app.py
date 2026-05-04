from flask import Flask, render_template, request
import os

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

# -----------------------------
# IMPORT AI MODULES
# -----------------------------
from models.sentiment_model import analyze_sentiment
from models.intent_detection import detect_intent
from models.rag_engine import generate_rag_response
from models.image_emotion import detect_image_emotion
from models.voice_emotion import detect_voice_emotion
from models.webcam_emotion import start_webcam_emotion

# -----------------------------
# FLASK APP
# -----------------------------
app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# CREATE FOLDERS
os.makedirs('static/uploads', exist_ok=True)
os.makedirs('static/charts', exist_ok=True)

# -----------------------------
# ALLOWED FILE TYPES
# -----------------------------
ALLOWED_IMAGE_EXTENSIONS = {
    'png',
    'jpg',
    'jpeg'
}

ALLOWED_AUDIO_EXTENSIONS = {
    'wav',
    'mp3'
}

def allowed_file(filename, allowed_extensions):

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

# -----------------------------
# CREATE CHART
# -----------------------------
def create_chart(
    sentiment,
    sentiment_score,
    image_emotion,
    image_conf,
    voice_emotion,
    voice_conf
):

    plt.clf()

    plt.figure(figsize=(8, 4))

    labels = []
    scores = []

    # TEXT
    if sentiment == "No Text":

        labels.append("Text: No Input")
        scores.append(0.0)

    else:

        labels.append(f"Text: {sentiment}")
        scores.append(sentiment_score)

    # IMAGE
    if image_emotion in [
        "No Image Uploaded",
        "Face Not Detected"
    ]:

        labels.append("Image: No Face")
        scores.append(0.0)

    else:

        labels.append(f"Image: {image_emotion}")
        scores.append(image_conf)

    # VOICE
    if voice_emotion in [
        "No Audio Uploaded",
        "No Voice"
    ]:

        labels.append("Voice: No Audio")
        scores.append(0.0)

    else:

        labels.append(f"Voice: {voice_emotion}")
        scores.append(voice_conf)

    # BAR CHART
    plt.barh(
        labels,
        scores,
        color=[
            '#38bdf8',
            '#a78bfa',
            '#22c55e'
        ]
    )

    plt.xlabel("Confidence Score")

    plt.xlim(0, 1)

    plt.title(
        "Multimodal Emotion Detection"
    )

    for i, v in enumerate(scores):

        plt.text(
            v + 0.02,
            i,
            f"{v:.2f}",
            va='center'
        )

    plt.tight_layout()

    chart_path = 'static/charts/chart.png'

    plt.savefig(chart_path)

    plt.close()

    return chart_path

# -----------------------------
# HOME ROUTE
# -----------------------------
@app.route('/')
def home():

    return render_template(
        'index.html'
    )

# -----------------------------
# WEBCAM ROUTE
# -----------------------------
@app.route('/webcam')
def webcam():

    start_webcam_emotion()

    return '''
    <h2>
    Webcam Closed Successfully
    </h2>
    '''

# -----------------------------
# ANALYZE ROUTE
# -----------------------------
@app.route(
    '/analyze',
    methods=['POST']
)
def analyze():

    # -----------------------------
    # TEXT INPUT
    # -----------------------------
    text = request.form.get('text')

    # -----------------------------
    # VOICE TEXT
    # -----------------------------
    voice_text = request.form.get(
        'voice_text'
    )

    text = (text or "").strip()

    voice_text = (
        voice_text or ""
    ).strip()

    if voice_text:

        text = text + " " + voice_text

    # -----------------------------
    # IMAGE FILE
    # -----------------------------
    image = request.files.get(
        'image'
    )

    # -----------------------------
    # AUDIO FILE
    # -----------------------------
    audio = request.files.get(
        'audio'
    )

    # -----------------------------
    # IMAGE EMOTION
    # -----------------------------
    image_emotion = (
        "No Image Uploaded"
    )

    image_conf = 0.0

    if image and allowed_file(
        image.filename,
        ALLOWED_IMAGE_EXTENSIONS
    ):

        image_path = os.path.join(
            app.config['UPLOAD_FOLDER'],
            image.filename
        )

        image.save(image_path)

        image_emotion, image_conf = \
            detect_image_emotion(
                image_path
            )

    # -----------------------------
    # VOICE EMOTION
    # -----------------------------
    voice_emotion = (
        "No Audio Uploaded"
    )

    voice_conf = 0.0

    if audio and allowed_file(
        audio.filename,
        ALLOWED_AUDIO_EXTENSIONS
    ):

        audio_path = os.path.join(
            app.config['UPLOAD_FOLDER'],
            audio.filename
        )

        audio.save(audio_path)

        voice_emotion, voice_conf = \
            detect_voice_emotion(
                audio_path
            )

    # -----------------------------
    # TEXT SENTIMENT
    # -----------------------------
    if not text or text.strip() == "":

        sentiment = "No Text"
        sentiment_score = 0.0

    else:

        sentiment, sentiment_score = \
            analyze_sentiment(text)

    # -----------------------------
    # INTENT DETECTION
    # -----------------------------
    intent = detect_intent(text)

    # -----------------------------
    # RAG RESPONSE
    # -----------------------------
    response = generate_rag_response(
        text,
        sentiment,
        intent
    )

    # -----------------------------
    # CREATE CHART
    # -----------------------------
    chart_path = create_chart(
        sentiment,
        sentiment_score,
        image_emotion,
        image_conf,
        voice_emotion,
        voice_conf
    )

    # -----------------------------
    # RETURN RESULTS
    # -----------------------------
    return render_template(
        'index.html',
        sentiment=sentiment,
        intent=intent,
        image_emotion=image_emotion,
        voice_emotion=voice_emotion,
        response=response,
        chart_path=chart_path
    )

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == '__main__':

    app.run(
        debug=True,
        threaded=True
    )

