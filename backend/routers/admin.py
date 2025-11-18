from fastapi import APIRouter
from backend.services.vector_builder import rebuild_vector_store
from backend.services.vector_store import load_in_memory_store

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/rebuild-vector-store")
async def rebuild_vector_store_handler():
    """
    Rebuilds the vector store and reloads it into memory.
    """
    try:
        rebuild_vector_store()          # writes vectors.json
        load_in_memory_store()          # loads into RAM
        return {"status": "Vector store rebuilt successfully"}
    except Exception as e:
        return {"error": str(e)}
