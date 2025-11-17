from fastapi import APIRouter

router = APIRouter()


@router.post("/tailor")
async def tailor_resume():
    return {"status": "tailor placeholder"}
