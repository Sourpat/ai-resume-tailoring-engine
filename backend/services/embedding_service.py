from openai import OpenAI
import os


class EmbeddingService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def embed_text(self, text: str):
        """
        Generate embeddings using OpenAI 'text-embedding-3-small'.
        """
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception:
            return []
