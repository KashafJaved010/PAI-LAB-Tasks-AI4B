
import os
import requests
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('NEWS_API_KEY')
print("DEBUG: API_KEY =", API_KEY)
NEWS_API_URL = 'https://newsapi.org/v2/top-headlines'

@app.route('/')
def index():
    if not API_KEY:
        error = "API key not found. Please set NEWS_API_KEY in .env file"
        return render_template('index.html', articles=[], error=error)

    params = {
        'country': 'us',
        'apiKey': API_KEY
    }

    articles = []
    error = None

    try:
        response = requests.get(NEWS_API_URL, params=params)
        data = response.json()

        if data.get('status') == 'ok':
            articles = data['articles']
        else:
            error = data.get('message', 'Unknown error from NewsAPI')
    except Exception as e:
        error = str(e)

    return render_template('index.html', articles=articles, error=error)

if __name__ == '__main__':
    app.run(debug=True)