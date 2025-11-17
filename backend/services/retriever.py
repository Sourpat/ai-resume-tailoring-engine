# backend/services/retriever.py

import os
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
VECTOR_STORE_PATH = BASE_DIR / "backend" / "vector_store"

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

        VECTOR_STORE_PATH.mkdir(exist_ok=True)
        store_file = VECTOR_STORE_PATH / "seed_vectors.json"
        seed_docs = Retriever.load_seed_documents()

        vectors = []
        for doc in seed_docs:
            embedding = Retriever.embed_text(doc["content"])
            vectors.append({
                "filename": doc["filename"],
                "embedding": embedding,
                "content": doc["content"]
            })

        with open(store_file, "w", encoding="utf-8") as f:
            json.dump(vectors, f, indent=2)

        print("Vector store updated successfully.")

    @staticmethod
    def search(query: str):
        store_file = VECTOR_STORE_PATH / "seed_vectors.json"
        if not store_file.exists():
            return []

        with open(store_file, "r", encoding="utf-8") as f:
            vectors = json.load(f)

        query_vector = Retriever.embed_text(query)

        def cosine_similarity(a, b):
            dot = sum(x * y for x, y in zip(a, b))
            norm_a = sum(x * x for x in a) ** 0.5
            norm_b = sum(x * x for x in b) ** 0.5
            return dot / (norm_a * norm_b)

        ranked = sorted(
            vectors,
            key=lambda x: cosine_similarity(query_vector, x["embedding"]),
            reverse=True,
        )
        return ranked[:5]
