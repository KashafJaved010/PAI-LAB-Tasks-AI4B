import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import os

# Load dataset with proper quoting
df = pd.read_csv('shopping_qna.csv', quoting=1)  # quoting=1 means QUOTE_ALL
questions = df['question'].tolist()
answers = df['answer'].tolist()

# Load MiniLM model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Encode questions
print("Encoding questions...")
embeddings = model.encode(questions, convert_to_numpy=True)
print(f"Embeddings shape: {embeddings.shape}")

# Save embeddings as .npy (optional)
np.save('shopping_embeddings.npy', embeddings)

# Create FAISS index (L2 distance)
dimension = embeddings.shape[1]
faiss_index = faiss.IndexFlatL2(dimension)
faiss_index.add(embeddings)

# Save FAISS index and metadata
os.makedirs('faiss_index', exist_ok=True)
faiss.write_index(faiss_index, 'faiss_index/shopping_index.bin')

with open('faiss_index/questions.pkl', 'wb') as f:
    pickle.dump(questions, f)
with open('faiss_index/answers.pkl', 'wb') as f:
    pickle.dump(answers, f)

print(f"Index built with {len(questions)} questions. Saved to faiss_index/")