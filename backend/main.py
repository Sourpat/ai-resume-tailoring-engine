import logging
import os
import sys

# Ensure the backend package is discoverable when uvicorn runs from within
# the backend directory (Render default) or the repository root.
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.routers import admin, debug, debug_ingest, export, tailor, test_routes, upload
from backend.vector_store.ingest import build_initial_vector_store
from backend.services.retriever import Retriever

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Resume Tailoring Engine")

app.include_router(upload.router)
app.include_router(tailor.router)
app.include_router(export.router)
app.include_router(admin.router)
app.include_router(debug.router)
app.include_router(debug_ingest.router, prefix="/debug")
app.include_router(test_routes.router, prefix="/test")


@app.on_event("startup")
async def startup_event():
    try:
        print("Running vector store ingestion...")
        build_initial_vector_store()
        print("Loading in-memory vector store...")
        Retriever.load_vector_store()
        print("Vector store initialized successfully.")
    except Exception as e:
        print("ERROR: Vector store failed to initialize:", e)


@app.get("/")
async def read_root():
    return {"message": "AI Resume Tailoring Engine API"}


@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Backend is running"}


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception", exc_info=exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
