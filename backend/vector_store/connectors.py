import json
import os
from typing import Any, Dict, List, Optional

from services.embedding_service import EmbeddingService

import numpy as np


class VectorDBConnector:
    """Placeholder in-memory vector database connector."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), "local_vector_db.json")
        self.vectors: List[Dict[str, Any]] = []
        self.embedding_service = EmbeddingService()
        self.load_local_db()

    def load_local_db(self) -> None:
        """Load vectors from a local JSON file into memory."""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    self.vectors = data.get("vectors", [])
            except (json.JSONDecodeError, OSError):
                self.vectors = []
        else:
            self.vectors = []

    def add_vector(self, item: Dict[str, Any]) -> None:
        """Add a vector item to the in-memory store."""
        self.vectors.append(item)

    def add_documents(self, documents: List[str]) -> None:
        """Embed and add a batch of text documents to the store."""
        starting_length = len(self.vectors)
        for index, document in enumerate(documents):
            embedding = self.embedding_service.embed_text(document)
            item = {
                "id": f"doc_{starting_length + index}",
                "content": document,
                "embedding": embedding,
            }
            self.add_vector(item)

    def query_vectors(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Return the ``top_k`` vectors ranked by cosine similarity."""
        if not query_embedding:
            return []

        ranked_vectors: List[Dict[str, Any]] = []
        for vector in self.vectors:
            embedding = vector.get("embedding", [])
            if not embedding:
                continue
            similarity = cosine_similarity(query_embedding, embedding)
            ranked_vectors.append({**vector, "similarity": similarity})

        ranked_vectors.sort(key=lambda item: item.get("similarity", 0.0), reverse=True)
        return ranked_vectors[:top_k]

    def save_local_db(self) -> None:
        """Persist the in-memory vectors to a local JSON file."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with open(self.db_path, "w", encoding="utf-8") as file:
            json.dump({"vectors": self.vectors}, file, indent=2)


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Calculate cosine similarity with a ZeroDivisionError guard."""
    if not a or not b:
        return 0.0

    vector_a = np.array(a)
    vector_b = np.array(b)
    denominator = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    if denominator == 0:
        return 0.0

    return float(np.dot(vector_a, vector_b) / denominator)
