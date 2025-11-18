# backend/services/retriever.py

from pathlib import Path
from typing import Any, List
from openai import OpenAI
from dotenv import load_dotenv
import json
import logging

load_dotenv()

client = OpenAI()

BASE_DIR = Path(__file__).resolve().parents[2]
SEED_DIR = BASE_DIR / "backend" / "seeds"
SEED_DIR.mkdir(parents=True, exist_ok=True)
print("Resolved SEED_DIR:", SEED_DIR)
VECTOR_STORE_DIR = BASE_DIR / "backend" / "vector_store"
VECTOR_STORE_PATH = VECTOR_STORE_DIR / "vectors.json"
vector_store = None

class Retriever:
    @staticmethod
    def embed_text(text: str):
        response = client.embeddings.create(
            model="text-embedding-3-large",
            input=text
        )
        return response.data[0].embedding

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 700, overlap: int = 100) -> List[str]:
        if chunk_size <= overlap:
            raise ValueError("chunk_size must be greater than overlap")

        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + chunk_size
            chunks.append(text[start:end])
            if end >= text_length:
                break
            start = end - overlap

        return chunks

    @staticmethod
    def load_seed_documents() -> List[dict]:
        documents = []
        for file in sorted(SEED_DIR.glob("*.txt")):
            logging.info("Ingesting seed file: %s", file.name)
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
                if not content:
                    continue
                documents.append({
                    "filename": file.name,
                    "content": content
                })
        return documents

    @staticmethod
    def rebuild_vector_store():
        logging.info("Rebuilding vector store...")

        VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
        logging.info("Vector store directory resolved to: %s", VECTOR_STORE_DIR)

        if VECTOR_STORE_PATH.exists():
            logging.info("Removing old vector store file: %s", VECTOR_STORE_PATH)
            VECTOR_STORE_PATH.unlink()

        index = []
        total_chunks = 0
        for path in sorted(SEED_DIR.glob("*.txt")):
            text = path.read_text(encoding="utf-8")
            if len(text) < 5:
                continue

            chunks = Retriever.chunk_text(text)
            logging.info("Embedding file %s into %d chunks", path.name, len(chunks))
            total_chunks += len(chunks)

            for chunk_index, chunk_text in enumerate(chunks):
                embedding = Retriever.embed_text(chunk_text)
                index.append({
                    "file": path.name,
                    "chunk_index": chunk_index,
                    "chunk_text": chunk_text,
                    "embedding": embedding,
                })

        global vector_store
        vector_store = {"vectors": index}

        with open(VECTOR_STORE_PATH, "w", encoding="utf-8") as f:
            json.dump(vector_store, f, indent=2)

        logging.info("Total chunks stored: %d", total_chunks)
        logging.info("Vector store built with %d items", len(index))

    @staticmethod
    def load_vector_store() -> dict:
        global vector_store

        VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

        def rebuild_with_warning(message: str):
            logging.warning(message)
            Retriever.rebuild_vector_store()

        if not VECTOR_STORE_PATH.exists() or VECTOR_STORE_PATH.stat().st_size == 0:
            rebuild_with_warning("Vector store file missing or empty; rebuilding vector store.")
            return vector_store

        try:
            with open(VECTOR_STORE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as exc:
            rebuild_with_warning(f"Failed to load vector store ({exc}); rebuilding vector store.")
            return vector_store

        if isinstance(data, dict) and data.get("vectors"):
            vector_store = data
        elif isinstance(data, list) and data:
            vector_store = {"vectors": data}
        else:
            rebuild_with_warning("Vector store file contained no vectors; rebuilding vector store.")

        if vector_store is None:
            rebuild_with_warning("Vector store not initialized; rebuilding vector store.")

        return vector_store

    @staticmethod
    def search(query: str):
        global vector_store

        if vector_store is None:
            Retriever.load_vector_store()

        query_vector = Retriever.embed_text(query)

        def cosine_similarity(a, b):
            if not a or not b:
                return 0

            dot = sum(x * y for x, y in zip(a, b))
            norm_a = sum(x * x for x in a) ** 0.5
            norm_b = sum(x * x for x in b) ** 0.5
            if norm_a == 0 or norm_b == 0:
                return 0

            return dot / (norm_a * norm_b)

        vectors = (vector_store or {}).get("vectors", [])
        ranked = []
        for item in vectors:
            similarity = cosine_similarity(query_vector, item.get("embedding", []))
            ranked.append({
                **item,
                "similarity": similarity,
            })

        ranked.sort(key=lambda x: x["similarity"], reverse=True)
        return ranked[:5]

    @staticmethod
    def debug_retrieve(query: str, vector_data: Any) -> dict:
        """
        Retrieve the most similar vectors from a preloaded vector store for debugging.

        Parameters
        ----------
        query: str
            The input query text.
        vector_data: Any
            Parsed JSON data representing the vector store. Expected to be either a
            list of vector entries or a dictionary containing a "vectors" key.
        """

        if isinstance(vector_data, dict):
            vectors = vector_data.get("vectors", [])
        elif isinstance(vector_data, list):
            vectors = vector_data
        else:
            vectors = []

        if not vectors:
            return {"matches": []}

        query_vector = Retriever.embed_text(query)

        def cosine_similarity(a, b):
            if not a or not b:
                return 0

            dot = sum(x * y for x, y in zip(a, b))
            norm_a = sum(x * x for x in a) ** 0.5
            norm_b = sum(x * x for x in b) ** 0.5
            if norm_a == 0 or norm_b == 0:
                return 0

            return dot / (norm_a * norm_b)

        ranked = []
        for item in vectors:
            embedding = item.get("embedding", []) if isinstance(item, dict) else []
            if not embedding:
                continue

            similarity = cosine_similarity(query_vector, embedding)
            ranked.append({
                "content": item.get("content"),
                "role": item.get("role"),
                "similarity": similarity,
            })

        ranked.sort(key=lambda x: x.get("similarity", 0), reverse=True)
        return {"matches": ranked[:5]}
