from fastapi import APIRouter
from services.retriever import Retriever

router = APIRouter()

@router.post("/admin/rebuild-vector-store")
def rebuild_vector_store():
    Retriever.rebuild_vector_store()
    return {"status": "Vector store rebuilt successfully"}
