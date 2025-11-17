Backend API for AI Resume Tailoring Engine built using FastAPI.

## Embedding & RAG Layer
- Uses OpenAI embeddings model: text-embedding-3-small
- Local cosine similarity search
- Seeds are loaded from /seeds folder and embedded
- RAGService.query() retrieves top matches

## Test Endpoints

### GET /health
Checks if backend is running.

### GET /test/rag-test?query=example
Tests vector store retrieval.

### POST /test/tailor-test
Runs the entire tailoring pipeline using a sample JD.

Logs are printed to console for debugging.
