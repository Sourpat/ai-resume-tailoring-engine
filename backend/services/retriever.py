# backend/services/retriever.py

from pathlib import Path
from typing import List
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
        for path in sorted(SEED_DIR.glob("*.txt")):
            text = path.read_text(encoding="utf-8")
            if len(text) < 5:
                continue

            print("Embedding file:", path.name)
            embedding = client.embeddings.create(
                model="text-embedding-3-large",
                input=text
            )
            print("Embedding length:", len(embedding.data[0].embedding))

            index.append({
                "file": path.name,
                "content": text,
                "embedding": embedding.data[0].embedding
            })

        with open(INDEX_PATH, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2)

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

        ranked = sorted(
            vectors,
            key=lambda x: cosine_similarity(query_vector, x.get("embedding", [])),
            reverse=True,
        )
        return ranked[:5]
