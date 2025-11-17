from pathlib import Path

from fastapi import APIRouter


router = APIRouter()

INGESTION_DIR = Path(__file__).resolve().parents[1] / "ingestion"
ALLOWED_EXTENSIONS = {".txt", ".md"}


@router.get("/ingest-files")
def list_ingestion_files():
    """List ingestion filenames without reading file contents."""
    if not INGESTION_DIR.exists() or not INGESTION_DIR.is_dir():
        return {"files": []}

    try:
        files = [
            path.name
            for path in sorted(INGESTION_DIR.iterdir())
            if path.is_file() and path.suffix.lower() in ALLOWED_EXTENSIONS
        ]
        return {"files": files}
    except Exception:
        # Defensive: avoid leaking file system details
        return {"files": []}
