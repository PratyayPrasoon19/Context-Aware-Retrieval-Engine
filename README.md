# Teleport Logistics Semantic RAG & Vector Search

## Project Overview

This project implements a local Retrieval-Augmented Generation (RAG) pipeline focused on semantic search over a logistics knowledge base. It demonstrates two retrieval strategies:

- Strategy A: Raw Vector Search (standard direct embedding retrieval)
- Strategy B: AI-Enhanced Retrieval (query enhancement before embedding)

The backend provides a REST API for querying the logistics knowledge base, while the frontend offers a simple React interface for user interaction.

## Architecture Overview

The application follows a modular architecture with clear separation of concerns:

### Backend Architecture

```
[User Query] → [Flask API] → [Handler] → [Query Expansion (Strategy B) / Direct (Strategy A)] → [RAG Pipeline] → [FAISS Vector DB] → [Results]
```

### Data Flow

1. **Data Ingestion**: Logistics knowledge base text is loaded and split into chunks using LangChain's RecursiveCharacterTextSplitter.
2. **Embedding Generation**: Chunks are encoded using SentenceTransformers (all-MiniLM-L6-v2) to simulate Vertex AI's textembedding-gecko.
3. **Vector Storage**: Embeddings are stored in FAISS (Facebook AI Similarity Search) for efficient similarity search.
4. **Query Processing**:
   - **Strategy A (Raw Vector Search)**: Direct embedding of the original user query followed by cosine similarity search in FAISS.
   - **Strategy B (AI-Enhanced Retrieval)**: Query expansion / enhancement is applied first, then the expanded query is embedded and searched. This strategy is obtained by query enhancement and is intended to improve retrieval alignment with the logistics knowledge base.
5. **Benchmarking**: Both strategies return top-3 results with scores for comparison, enabling analysis of how query enhancement changes retrieval quality.

### Architecture Diagram

```mermaid
graph TD
    A[User Query] --> B[Flask API /search]
    B --> C[Handler]
    C --> D{Strategy Selection}
    D --> E[Strategy A: Direct Retrieval]
    D --> F[Strategy B: Query Expansion]
    F --> G[LLM-Based Semantic Query Rewriting]
    G --> H[Retrieval Pipeline]
    E --> H
    H --> I[Encode Query with SentenceTransformers]
    I --> J[FAISS Cosine Similarity Search]
    J --> K[Top-3 Results]
    K --> L[Structured JSON Response]
    L --> M[Frontend Display]

    subgraph "Data Preparation"
        N[Logistics Knowledge Base] --> O[RecursiveCharacterTextSplitter]
        O --> P[SentenceTransformers Embedding]
        P --> Q[FAISS Index Creation]
    end
```

## Project Structure

```
Teleport_Assignement/
├── backend/
│   ├── main.py                 # Flask application entry point
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables
│   ├── api/
│   │   └── endpoints.py        # API routes (/search)
│   ├── config/
│   │   └── config.py           # Configuration loading
│   ├── docs/
│   │   └── logistics_knowledge_base.txt  # Knowledge base data
│   └── pkg/
│       ├── handler/
│       │   └── handler.py      # Request handling logic
│       └── services/
│           ├── query_expansion.py  # Query expansion service
│           └── rag_pipeline.py     # RAG pipeline implementation
├── frontend/
│   ├── package.json            # Node.js dependencies and scripts
│   ├── public/
│   │   ├── index.html
│   │   └── ...
│   └── src/
│       ├── App.js              # Main React component
│       └── ...
└── README.md                   # This file
```

## Backend Details

### Core Components

- **main.py**: Initializes Flask app with CORS support and registers API blueprint.
- **api/endpoints.py**: Defines `/api/search` POST endpoint for queries.
- **config/config.py**: Loads environment variables, sets PORT and GEMINI_API_KEY.
- **pkg/handler/handler.py**: Orchestrates both retrieval strategies and formats comparison response.
- **pkg/services/query_expansion.py**: Implements rule-based query expansion with logistics-specific synonyms.
- **pkg/services/rag_pipeline.py**: Manages data ingestion, embedding generation, FAISS indexing, and retrieval.

### Technologies Used

- **Flask**: Lightweight web framework for API
- **FAISS**: Efficient vector similarity search
- **SentenceTransformers**: Local embedding model (all-MiniLM-L6-v2)
- **LangChain**: Text splitting utilities
- **NumPy**: Numerical operations for embeddings

## Frontend Details

The frontend is a minimal React application that provides a simple interface to interact with the backend API. It includes basic components for query input and result display.

### Technologies Used

- **React**: UI framework
- **React Scripts**: Build and development tools

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 14+
- Git

### Environment Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Initialize Backend Environment:
   ```bash
   cd backend
   # Create .env file
   cp .env.example .env
   ```

   Edit `.env` file:
   ```
   PORT=5000
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```

3. Install Backend Dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize Frontend Environment:
   ```bash
   cd ../frontend
   npm install
   ```

### Running the Application

1. Start Backend:
   ```bash
   cd backend
   python main.py
   ```
   The backend will run on http://localhost:5000

2. Start Frontend (in a new terminal):
   ```bash
   cd frontend
   npm start
   ```
   The frontend will run on http://localhost:3000

## Usage

1. Open the frontend in your browser (http://localhost:3000)
2. Enter a query related to logistics (e.g., "How does the system handle peak load?")
3. The application will return results from both retrieval strategies for comparison

### API Usage

Send POST requests to `http://localhost:5000/api/search` with JSON body:
```json
{
  "query": "How does the system handle peak load?"
}
```

Response format:
```json
{
  "query": "How does the system handle peak load?",
  "result": [
    {
      "type": "regular_result",
      "response": [
        {"query": "chunk text", "rank": 1, "score": 0.85},
        ...
      ]
    },
    {
      "type": "expanded_result",
      "response": [
        {"query": "chunk text", "rank": 1, "score": 0.82},
        ...
      ]
    }
  ]
}
```

## Benchmarking

The application automatically compares two retrieval strategies:

- **Strategy A (Raw Vector Search)**: Direct embedding-based similarity search using the raw user query.
- **Strategy B (AI-Enhanced Retrieval)**: Query enhancement is applied before embedding, improving the query's semantic density and alignment with the knowledge base.

Sample comparison results from evaluation queries:

| Query | Strategy A score | Strategy B score | Improvement |
|---|---|---|---|
| How does the system handle peak delivery demand? | 0.5354 | 0.7009 | +0.1655 |
| What happens if a warehouse becomes overloaded | 0.5329 | 0.6953 | +0.1624 |
| How are fleet resources dynamically allocated during demand surges | 0.5470 | 0.6455 | +0.0985 |
| How does the system maintain real-time shipment visibility | 0.4581 | 0.6496 | +0.1915 |
| How are API overloads and traffic spikes handled | 0.4722 | 0.6194 | +0.1472 |
| How does the system maintain synchronization across distributed regions | 0.4384 | 0.6259 | +0.1875 |

Average improvement observed across sample queries: **+0.1588**.

Results include top-3 chunks with similarity scores for each strategy, enabling evaluation of retrieval quality improvements through query expansion.

### Technical Requirements Met

1. **Embedding Model**: Uses SentenceTransformers (all-MiniLM-L6-v2) to simulate Vertex AI's textembedding-gecko behavior.

2. **Vector Database**: Implements FAISS for lightweight local vector storage and search.

3. **Mocking**: Query expansion uses rule-based synonym addition instead of actual LLM calls, simulating AI-enhanced retrieval.

4. **Orchestration**: Python classes manage data ingestion from the logistics knowledge base text file.

### Benchmarking Task

The `/api/search` endpoint outputs structured JSON comparing both strategies for each query, showing:
- Original query
- Top 3 chunks from Strategy A with similarity scores
- Top 3 chunks from Strategy B (after query expansion) with similarity scores

### Production Migration Path

To migrate this system to Vertex AI Vector Search (Matching Engine) in production:
1. Replace the local SentenceTransformers model with Vertex AI `TextEmbeddingModel` (for example, `textembedding-gecko`).
2. Use Vertex AI Vector Search / Matching Engine to create and manage a vector index instead of FAISS.
3. Store document chunk metadata alongside vectors so the system can return text chunks and rankings in search results.
4. Keep cosine similarity or dot-product matching as the metric, since Vertex AI matching supports both and cosine is preferred for embeddings.
5. Implement actual LLM-based query expansion using Vertex AI Generative Models, rather than rule-based expansion.
6. Deploy the backend in a GCP environment with proper IAM, logging, monitoring, and batching for inference throughput.

### Test Coverage

This project includes Pytest suites for:
- verifying the retrieval pipeline logic and indexing behavior,
- ensuring similarity scoring works as expected,
- mocking the GCP SDK (`google.generativeai`) during query expansion.

### Dev Evidence

A `retrieval_benchmark.md` file is included in the repository showing the output of the Strategy A vs Strategy B comparison. This file documents the evaluation results from sample queries and captures the improvement achieved by query enhancement.

### Repository Contents

- **Source Code**: Modular Python files in `backend/pkg/` for embedding, storage, and retrieval
- **Tests**: Pytest suites are available in `backend/tests/`
- **Dev Evidence**: `retrieval_benchmark.md` records the sample Strategy A vs Strategy B comparison
- **Documentation**: This README explains implementation choices, similarity metric selection, and Vertex AI migration path

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with proper testing
4. Submit a pull request
