from backend.vector_store.connectors import VectorDBConnector


class RAGService:
    def __init__(self):
        self.db = VectorDBConnector()

    def retrieve(self, query: str = ""):
        return {
            "matches": [
                {"role": "placeholder", "content": "sample seed"}
            ]
        }
