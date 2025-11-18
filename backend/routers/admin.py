from fastapi import APIRouter

# Correct imports for Render directory structure
from services.vector_builder import rebuild_vector_store
from services.rag_service import load_in_memory_store

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/rebuild-vector-store")
async def rebuild_vector_store_handler():
    try:
        rebuild_vector_store()
        load_in_memory_store()
        return {"status": "Vector store rebuilt successfully"}
    except Exception as e:
        return {"error": str(e)}
