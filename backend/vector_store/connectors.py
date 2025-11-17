import json
import os
from typing import Any, Dict, List, Optional


class VectorDBConnector:
    """Placeholder in-memory vector database connector."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), "local_vector_db.json")
        self.vectors: List[Dict[str, Any]] = []
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

    def query_vectors(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Return the first ``top_k`` vectors as placeholder matches."""
        return self.vectors[:top_k]

    def save_local_db(self) -> None:
        """Persist the in-memory vectors to a local JSON file."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with open(self.db_path, "w", encoding="utf-8") as file:
            json.dump({"vectors": self.vectors}, file, indent=2)
