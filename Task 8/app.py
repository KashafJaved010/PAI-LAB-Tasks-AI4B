import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = os.getenv('NEWS_API_KEY')
NEWS_API_URL = 'https://newsapi.org/v2/top-headlines'
EVERYTHING_URL = 'https://newsapi.org/v2/everything'
PAGE_SIZE = 10  # articles per page

def fetch_news(params):
    """Fetch news and return (articles, total_results, error)"""
    try:
        resp = requests.get(params['url'], params=params['query'], timeout=10)
        data = resp.json()
        if data.get('status') == 'ok':
            return data['articles'], data.get('totalResults', 0), None
        return [], 0, data.get('message', 'Unknown error')
    except Exception as e:
        return [], 0, str(e)

@app.route('/')
def index():
    if not API_KEY:
        return render_template('index.html', error="API key missing. Set NEWS_API_KEY in .env")

    # Get request args with defaults
    country = request.args.get('country', 'us')
    category = request.args.get('category', 'general')
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)

    # Basic validation
    valid_countries = ['us','gb','in','ca','au','pk','tr'] # add more if needed
    if country not in valid_countries:
        country = 'us'
    valid_categories = ['general', 'business', 'technology', 'sports', 'health', 'science', 'entertainment']
    if category not in valid_categories:
        category = 'general'

    # Build API parameters
    params = {
        'apiKey': API_KEY,
        'pageSize': PAGE_SIZE,
        'page': page,
        'country': country,
        'category': category
    }
    if query:
        url = EVERYTHING_URL
        params.update({'q': query, 'sortBy': 'publishedAt', 'language': 'en'})
    else:
        # url = NEWS_API_URL
        # params.update({'country': country, 'category': category})
        url = NEWS_API_URL

    # Fetch news
    articles, total_results, error = fetch_news({'url': url, 'query': params})

    # Pagination calculations
    total_pages = (total_results + PAGE_SIZE - 1) // PAGE_SIZE if total_results else 1
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    return render_template('index.html',
                           articles=articles,
                           error=error,
                           country=country,
                           category=category,
                           query=query,
                           page=page,
                           prev_page=prev_page,
                           next_page=next_page,
                           total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True, port=5001)