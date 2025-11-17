import base64
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from agents.export_agent import ExportAgent

router = APIRouter()


class ExportRequest(BaseModel):
    po: List[str]
    ba: List[str]
    technical_ba: List[str]


@router.post("/export")
async def export_resume(request: ExportRequest):
    export_agent = ExportAgent()
    export_result = export_agent.run(request.model_dump())

    return {
        "markdown": export_result.get("md", ""),
        "docx_base64": export_result.get("docx", base64.b64encode(b"").decode("utf-8")),
        "pdf_base64": export_result.get("pdf", base64.b64encode(b"").decode("utf-8")),
    }
