from fastapi import APIRouter
from pydantic import BaseModel

from services.agent_orchestrator import AgentOrchestrator

router = APIRouter()


class TailorRequest(BaseModel):
    jd_text: str


@router.post("/tailor")
async def tailor_resume(payload: TailorRequest):
    orchestrator = AgentOrchestrator()
    return orchestrator.run_pipeline(payload.jd_text)
