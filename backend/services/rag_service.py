from services.embedding_service import EmbeddingService
from vector_store.connectors import VectorDBConnector


class RAGService:
    def __init__(self):
        self.db = VectorDBConnector()
        self.embedding_service = EmbeddingService()

    def retrieve(self, query: str = ""):
        query_embedding = self.embedding_service.embed_text(query)
        results = self.db.query_vectors(query_embedding, top_k=5)

        matches = [
            {
                "role": item.get("role"),
                "content": item.get("content"),
                "similarity": item.get("similarity", 0.0),
            }
            for item in results
        ]

        return {"matches": matches}
