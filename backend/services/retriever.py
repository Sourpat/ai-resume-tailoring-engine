# backend/services/retriever.py

from pathlib import Path
from typing import Any, List
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()

BASE_DIR = Path(__file__).resolve().parents[2]
SEED_DIR = BASE_DIR / "backend" / "seeds"
SEED_DIR.mkdir(parents=True, exist_ok=True)
print("Resolved SEED_DIR:", SEED_DIR)
VECTOR_STORE_DIR = BASE_DIR / "backend" / "vector_store"
INDEX_PATH = VECTOR_STORE_DIR / "index.json"

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
            print("Ingesting seed file:", file.name)
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
        print("Rebuilding vector store...")

        VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

        index = []
        total_chunks = 0
        for path in sorted(SEED_DIR.glob("*.txt")):
            text = path.read_text(encoding="utf-8")
            if len(text) < 5:
                continue

            chunks = Retriever.chunk_text(text)
            print(f"Embedding file: {path.name} -> {len(chunks)} chunks")
            total_chunks += len(chunks)

            for chunk_index, chunk_text in enumerate(chunks):
                embedding = Retriever.embed_text(chunk_text)
                index.append({
                    "file": path.name,
                    "chunk_index": chunk_index,
                    "chunk_text": chunk_text,
                    "embedding": embedding,
                })

        with open(INDEX_PATH, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2)

        print(f"Total chunks stored: {total_chunks}")
        print(f"Vector store built with {len(index)} items")

    @staticmethod
    def load_index() -> List[dict]:
        if not INDEX_PATH.exists():
            return []

        try:
            with open(INDEX_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except (json.JSONDecodeError, OSError):
            return []

        return []

    @staticmethod
    def search(query: str):
        vectors = Retriever.load_index()
        if not vectors:
            return []

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
