import os
import time

from openai import OpenAI


class EmbeddingService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def embed_text(self, text: str):
        """
        Generate embeddings using OpenAI 'text-embedding-3-small'.
        """
        for attempt in range(5):
            try:
                response = self.client.embeddings.create(
                    model="text-embedding-3-small",
                    input=text
                )
                return response.data[0].embedding
            except Exception as e:
                if "429" in str(e):
                    time.sleep(1.5 ** attempt)
                    continue
                return []
        return []
