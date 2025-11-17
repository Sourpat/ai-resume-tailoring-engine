from pathlib import Path
from typing import List

from .connectors import VectorDBConnector


SEED_DIR = Path("backend/seeds")


def load_seed_documents() -> List[str]:
    docs = []
    for f in SEED_DIR.glob("*.txt"):
        docs.append(f.read_text(encoding="utf-8"))
    return docs


def build_initial_vector_store() -> VectorDBConnector:
    """Populate a local vector store from seed files."""
    connector = VectorDBConnector()
    docs = load_seed_documents()
    connector.add_documents(docs)
    connector.save_local_db()
    print(f"Vector store built with {len(connector.vectors)} items.")
    return connector


if __name__ == "__main__":
    build_initial_vector_store()
