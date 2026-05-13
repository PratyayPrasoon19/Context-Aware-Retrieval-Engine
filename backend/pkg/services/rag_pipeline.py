import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Global variables
model = SentenceTransformer('all-MiniLM-L6-v2')
file_path = r"docs\logistics_knowledge_base.txt"
chunks = None
index = None

def load_and_prepare_db(file_path):
    global chunks, index
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        separators=["\n## ", "\n### ", "\n\n", "\n"]
    )
    chunks = splitter.split_text(text)
    
    embeddings = model.encode(chunks)
    embeddings = np.array(embeddings).astype('float32')
    faiss.normalize_L2(embeddings)
    
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

def retrieval_pipeline(query, top_k=3):
    """The standard RAG retrieval flow."""
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype('float32')
    faiss.normalize_L2(query_embedding)
    
    distances, indices = index.search(query_embedding, top_k)
    
    results = []
    for i in range(len(indices[0])):
        idx = indices[0][i]
        results.append({
            "chunk": chunks[idx],
            "score": float(distances[0][i])
        })
    return results

# Initialize DB once
load_and_prepare_db(file_path)