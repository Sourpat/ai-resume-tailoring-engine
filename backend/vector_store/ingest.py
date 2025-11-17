import os
from typing import Dict, List

from services.embedding_service import EmbeddingService
from .connectors import VectorDBConnector


SEEDS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "seeds"))


def load_seeds() -> List[Dict[str, object]]:
    """Load seed markdown files and attach embeddings."""
    seeds: List[Dict[str, object]] = []
    if not os.path.isdir(SEEDS_DIR):
        return seeds

    embedding_service = EmbeddingService()

    for filename in os.listdir(SEEDS_DIR):
        if filename.endswith(".md"):
            file_path = os.path.join(SEEDS_DIR, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            embedding = embedding_service.embed_text(content)
            seeds.append(
                {
                    "id": filename,
                    "role": os.path.splitext(filename)[0],
                    "content": content,
                    "embedding": embedding,
                }
            )
    return seeds


def build_initial_vector_store() -> VectorDBConnector:
    """Populate a local vector store from seed files."""
    connector = VectorDBConnector()
    seeds = load_seeds()
    for seed in seeds:
        connector.add_vector(seed)
    connector.save_local_db()
    print(f"Vector store built with {len(seeds)} items.")
    return connector


if __name__ == "__main__":
    build_initial_vector_store()
