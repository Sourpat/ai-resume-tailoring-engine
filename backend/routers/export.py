from fastapi import APIRouter

router = APIRouter()


@router.post("/export")
async def export_resume():
    return {"status": "export placeholder"}
