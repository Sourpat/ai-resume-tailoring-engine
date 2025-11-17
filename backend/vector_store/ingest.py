from pathlib import Path
from typing import List

from services.logging_service import LoggingService

from .connectors import VectorDBConnector


BASE_DIR = Path(__file__).resolve().parents[2]
SEED_DIR = BASE_DIR / "backend" / "seeds"
SEED_DIR.mkdir(parents=True, exist_ok=True)
print("Resolved SEED_DIR:", SEED_DIR)
logger = LoggingService()


def load_seed_documents() -> List[str]:
    docs: List[str] = []
    if not SEED_DIR.exists():
        logger.log_error(f"Seed directory not found: {SEED_DIR}")
        return docs

    for seed_file in sorted(SEED_DIR.glob("*.txt")):
        try:
            logger.log_info(f"Ingesting seed file: {seed_file.name}")
            content = seed_file.read_text(encoding="utf-8")
            if not content:
                logger.log_error(f"Seed file {seed_file} is empty; skipping")
                continue
            docs.append(content)
        except OSError as exc:  # pragma: no cover - defensive
            logger.log_error(f"Failed to read seed file {seed_file}: {exc}")
    return docs


def build_initial_vector_store() -> VectorDBConnector:
    """Populate a local vector store from seed files."""
    connector = VectorDBConnector()
    docs = load_seed_documents()
    if not docs:
        logger.log_error("No seed documents found; skipping vector store build.")
        return connector

    connector.add_documents(docs)
    connector.save_local_db()
    logger.log_info(f"Vector store built with {len(connector.vectors)} items.")
    return connector


if __name__ == "__main__":
    build_initial_vector_store()
