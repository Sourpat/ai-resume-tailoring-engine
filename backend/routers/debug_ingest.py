from fastapi import APIRouter

from vector_store.ingest import SEED_DIR


router = APIRouter()


@router.get("/ingest-files")
def list_ingestion_files():
    """List ingestion filenames without reading file contents."""
    if not SEED_DIR.exists() or not SEED_DIR.is_dir():
        return {"files": []}

    try:
        files = [
            path.name
            for path in sorted(SEED_DIR.glob("*.txt"))
            if path.is_file()
        ]
        return {"files": files}
    except Exception:
        # Defensive: avoid leaking file system details
        return {"files": []}
