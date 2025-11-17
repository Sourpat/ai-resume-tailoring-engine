from fastapi import APIRouter, Query

from backend.services.agent_orchestrator import AgentOrchestrator
from backend.services.embedding_service import EmbeddingService
from backend.services.logging_service import LoggingService
from backend.vector_store.connectors import VectorDBConnector

router = APIRouter()
logger = LoggingService()
embedding_service = EmbeddingService()
vector_db = VectorDBConnector()


@router.get("/rag-test")
async def rag_test(query: str = Query("", description="Query text for RAG test")):
    try:
        logger.log_info("Running RAG test retrieval")
        query_embedding = embedding_service.embed_text(query)
        results = vector_db.query_vectors(query_embedding, top_k=5)
        matches = [
            {
                "content": item.get("content"),
                "role": item.get("role"),
                "similarity": item.get("similarity", 0.0),
            }
            for item in results
        ]
        logger.log_debug(f"RAG test matches: {matches}")
        return {"matches": matches}
    except Exception as exc:  # pragma: no cover - defensive
        logger.log_error(f"RAG test failed: {exc}")
        return {"matches": []}


@router.post("/tailor-test")
async def tailor_test():
    sample_jd = (
        "We are seeking a business analyst to collaborate with product teams, gather "
        "requirements, and support technical delivery. Experience with Agile practices, "
        "stakeholder communication, and documentation is preferred."
    )

    try:
        logger.log_info("Running tailoring pipeline test")
        orchestrator = AgentOrchestrator()
        result = orchestrator.run_pipeline(sample_jd)
        logger.log_debug(f"Tailor test result: {result}")

        exports = result.get("exports") or {}

        return {
            "jd_analysis": result.get("jd_analysis"),
            "retrieved_seeds": result.get("retrieved_seeds"),
            "tailored_bullets": result.get("tailored_bullets"),
            "formatted_output": result.get("formatted_output"),
            "exports": {"md_structure": exports.get("md_structure")},
        }
    except Exception as exc:  # pragma: no cover - defensive
        logger.log_error(f"Tailor test failed: {exc}")
        return {"error": "Tailor test failed"}
