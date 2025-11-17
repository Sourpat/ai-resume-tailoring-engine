Backend API for AI Resume Tailoring Engine built using FastAPI.

## Embedding & RAG Layer
- Uses OpenAI embeddings model: text-embedding-3-small
- Local cosine similarity search
- Seeds are loaded from /seeds folder and embedded
- RAGService.query() retrieves top matches
