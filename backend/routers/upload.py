from fastapi import APIRouter

router = APIRouter()


@router.post("/upload-resume")
async def upload_resume():
    return {"status": "ok"}
