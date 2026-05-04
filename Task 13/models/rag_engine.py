import os
import re
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# -----------------------------
# KNOWLEDGE BASE
# -----------------------------
KB_PATH = 'data/knowledge_base.txt'
knowledge_base = []
if os.path.exists(KB_PATH):
    with open(KB_PATH, 'r', encoding='utf-8') as f:
        knowledge_base = [p.strip() for p in f.read().split('\n\n') if p.strip()]
else:
    alt = 'data/knowledge_base'
    if os.path.exists(alt):
        with open(alt, 'r', encoding='utf-8') as f:
            knowledge_base = [p.strip() for p in f.read().split('\n\n') if p.strip()]
print(f"✅ Loaded {len(knowledge_base)} knowledge chunks")

# -----------------------------
# EMBEDDINGS & FAISS
# -----------------------------
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
index = None
if knowledge_base:
    embeddings = embedding_model.encode(knowledge_base)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings.astype('float32'))

# -----------------------------
# RETRIEVAL
# -----------------------------
def retrieve(query, top_k=1):
    if index is None or not knowledge_base:
        return ""
    q_emb = embedding_model.encode([query]).astype('float32')
    distances, indices = index.search(q_emb, top_k)
    chunks = [knowledge_base[i] for i in indices[0] if i < len(knowledge_base)]
    return "\n".join(chunks)

# -----------------------------
# CHECK IF IT'S A QUESTION (to use RAG)
# -----------------------------
def is_factual_question(text):
    text_lower = text.lower().strip()
    question_starters = ['what is', 'what are', 'define', 'how to', 'how does', 'why does', 'explain']
    return any(text_lower.startswith(q) for q in question_starters)

# -----------------------------
# MAIN FUNCTION – all emotions + RAG for questions
# -----------------------------
def generate_rag_response(user_text, sentiment, intent):
    if not user_text or not user_text.strip():
        return "Please tell me how you're feeling."

    text = user_text.lower().strip()

    # ----- FIRST: If it's a factual question, go directly to RAG -----
    if is_factual_question(text):
        retrieved = retrieve(user_text, top_k=1)
        if retrieved:
            answer = retrieved.split('.')[0] + '.'
            return f"{answer} (Retrieved from knowledge base)"
        else:
            return "I don't have specific info on that. Can I help with emotions instead?"

    # ----- EMOTION OVERRIDES (all common emotions) -----
    # Negative / distressed emotions
    if any(w in text for w in ['sad', 'depressed', 'unhappy', 'down', 'gloomy']):
        return "I'm sorry you're feeling sad or depressed. It's okay to feel that way. Do you want to talk about what's bothering you?"

    if any(w in text for w in ['tired', 'exhausted', 'drained', 'no energy']):
        return "It sounds like you're feeling tired. Make sure to rest and take breaks. I'm here for you."

    if any(w in text for w in ['stress', 'stressed', 'overwhelmed', 'pressure']):
        return "I hear that you're feeling stressed. Take a deep breath. Would you like some tips to manage stress?"

    if any(w in text for w in ['anxious', 'anxiety', 'nervous', 'worried']):
        return "Anxiety can be tough. Grounding techniques and deep breathing might help. I'm here to listen."

    if any(w in text for w in ['angry', 'mad', 'frustrated', 'annoyed', 'irritated']):
        return "I understand you're frustrated or angry. Take a moment to breathe. How can I help you calm down?"

    if any(w in text for w in ['hate', 'bad product', 'terrible', 'useless', 'awful']):
        return "I'm sorry you're unhappy with that. Can you tell me what went wrong? I'm here to help."

    if any(w in text for w in ['scared', 'fear', 'afraid', 'terrified']):
        return "Feeling scared is normal. You're not alone. What's making you feel this way?"

    if any(w in text for w in ['lonely', 'alone', 'isolated']):
        return "Loneliness can be hard. Remember that someone cares about you. Would you like to talk?"

    # Positive emotions
    if any(w in text for w in ['happy', 'joy', 'wonderful', 'great', 'amazing', 'fantastic']):
        return "That's wonderful! I'm glad you're feeling positive. Keep smiling! 😊"

    # Neutral / greetings (will fallback to RAG if not overridden)
    # But we add a simple greeting to be friendly
    if any(w in text for w in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
        return "Hello! How are you feeling today?"

    # ----- FALLBACK: Use RAG for anything else -----
    retrieved = retrieve(user_text, top_k=1)
    if retrieved:
        answer = retrieved.split('.')[0] + '.'
        return f"{answer} (From my knowledge base)"
    else:
        return "I'm here to listen. Can you tell me more about how you're feeling?"

