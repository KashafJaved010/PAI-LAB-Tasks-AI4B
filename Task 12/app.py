from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np

app = Flask(__name__)

# Load model and FAISS index (same as HadithBot)
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
faiss_index = faiss.read_index('faiss_index/shopping_index.bin')
with open('faiss_index/questions.pkl', 'rb') as f:
    questions = pickle.load(f)
with open('faiss_index/answers.pkl', 'rb') as f:
    answers = pickle.load(f)

def get_best_answer(query, top_k=1):
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = faiss_index.search(query_embedding, top_k)
    best_idx = indices[0][0]
    # Optional: distance threshold (like HadithBot didn't use)
    return answers[best_idx]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_query = data.get('query', '')
    if not user_query:
        return jsonify({'answer': 'Please ask a question about products, prices, or brands.'})
    try:
        answer = get_best_answer(user_query)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'answer': f'Sorry, error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)