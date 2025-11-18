import json
from pathlib import Path

from fastapi import APIRouter, Query

from services.agent_orchestrator import AgentOrchestrator
from services.logging_service import LoggingService
from services.retriever import Retriever

router = APIRouter()
logger = LoggingService()
TEST_VECTOR_PATH = Path(__file__).resolve().parent.parent / "vector_store" / "vectors.json"


@router.get("/rag-test")
async def rag_test(query: str = Query("", description="Query text for RAG test")):
    try:
        logger.log_info("Running RAG test retrieval")

        if not TEST_VECTOR_PATH.exists():
            logger.log_error(f"Vector store not found at {TEST_VECTOR_PATH}")
            return {"matches": []}

        with open(TEST_VECTOR_PATH, "r", encoding="utf-8") as file:
            vector_data = json.load(file)

        result = Retriever.debug_retrieve(query, vector_data)
        logger.log_debug(f"RAG test matches: {result}")
        return result
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
