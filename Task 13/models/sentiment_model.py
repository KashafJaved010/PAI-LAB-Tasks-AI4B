from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    if not text or text.strip() == "":
        return "No Text", 0.0
    result = sentiment_pipeline(text)
    sentiment = result[0]['label']   # POSITIVE / NEGATIVE
    score = result[0]['score']       # confidence
    return sentiment, score

