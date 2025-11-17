from services.rag_service import RAGService


class RagRetrieverAgent:
    def __init__(self):
        self.rag_service = RAGService()

    def run(self, jd_analysis: dict) -> dict:
        query = jd_analysis.get("JD_summary", "") if isinstance(jd_analysis, dict) else ""
        try:
            results = self.rag_service.retrieve(query=query)
            seeds = results.get("matches", []) if isinstance(results, dict) else []
        except Exception:
            seeds = []

        return {"retrieved_seeds": seeds}
