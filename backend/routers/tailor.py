from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.agent_orchestrator import AgentOrchestrator

router = APIRouter()


class TailorRequest(BaseModel):
    jd_text: str


@router.post("/tailor")
async def tailor_resume(payload: TailorRequest):
    orchestrator = AgentOrchestrator()
    result = orchestrator.run_pipeline(payload.jd_text)

    if result.get("error"):
        raise HTTPException(status_code=500, detail=result["details"])

    return result
