import faiss
import numpy as np

# Simple in-memory store for demo
vector_stores = {}
text_chunks = {}

def store_embeddings(session_id, embeddings, text):
    vectors = np.array([emb for _, emb in embeddings]).astype('float32')
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    vector_stores[session_id] = index
    text_chunks[session_id] = [chunk for chunk, _ in embeddings]

def query_embeddings(session_id, question):
    from embedder import model
    index = vector_stores[session_id]
    chunks = text_chunks[session_id]
    q_emb = model.encode([question]).astype('float32')
    D, I = index.search(q_emb, 3)
    return [chunks[i] for i in I[0]]
