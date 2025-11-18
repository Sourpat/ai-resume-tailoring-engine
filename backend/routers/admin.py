from fastapi import APIRouter

from backend.services.retriever import Retriever

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/rebuild-vector-store")
async def rebuild_vector_store_handler():
    try:
        Retriever.rebuild_vector_store()
        Retriever.load_vector_store()
        return {"status": "Vector store rebuilt successfully"}
    except Exception as e:
        return {"error": str(e)}
