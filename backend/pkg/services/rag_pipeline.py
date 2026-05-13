import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter


class MockTextEmbeddingModel:
    """
    Mocked Vertex AI TextEmbeddingModel abstraction.
    Simulates embedding generation behavior locally.
    """

    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def get_embeddings(self, texts):
        return self.model.encode(texts)


class SemanticRAGPipeline:
    """
    Enterprise Semantic RAG Pipeline

    Handles:
    - document ingestion
    - chunking
    - embedding generation
    - FAISS vector indexing
    - semantic retrieval
    """

    def __init__(self, file_path):
        self.file_path = file_path

        # Mocked embedding model
        self.embedding_model = MockTextEmbeddingModel()

        # Runtime objects
        self.chunks = []
        self.index = None

    def load_and_prepare_db(self):
        """
        Loads knowledge base,
        chunks documents,
        generates embeddings,
        and builds FAISS index.
        """

        with open(self.file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=120,
            separators=[
                "\n## ",
                "\n### ",
                "\n\n",
                "\n"
            ]
        )

        self.chunks = splitter.split_text(text)

        embeddings = self.embedding_model.get_embeddings(self.chunks)

        embeddings = np.array(embeddings).astype('float32')

        # Normalize for cosine similarity
        faiss.normalize_L2(embeddings)

        dimension = embeddings.shape[1]

        # Inner Product + normalized vectors = cosine similarity
        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(embeddings)

        print(f"[INFO] FAISS index initialized with {len(self.chunks)} chunks")

    def retrieval_pipeline(self, query, top_k=3):
        """
        Standard semantic retrieval pipeline.
        """

        if self.index is None:
            raise Exception("Vector database not initialized")

        query_embedding = self.embedding_model.get_embeddings([query])

        query_embedding = np.array(query_embedding).astype('float32')

        faiss.normalize_L2(query_embedding)

        distances, indices = self.index.search(query_embedding, top_k)

        results = []

        for i in range(len(indices[0])):

            idx = indices[0][i]

            results.append({
                "chunk": self.chunks[idx],
                "score": float(distances[0][i]),
                "rank": i + 1
            })

        return results


# Singleton pipeline instance
rag_pipeline = SemanticRAGPipeline(
    file_path=r"docs\logistics_knowledge_base.txt"
)