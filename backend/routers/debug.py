from pathlib import Path

from fastapi import APIRouter

from backend.services.logging_service import LoggingService
from backend.vector_store.connectors import VectorDBConnector
from backend.vector_store.ingest import SEED_DIR


router = APIRouter()
logger = LoggingService()


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _path_info(path: Path) -> dict:
    return {
        "path": str(path),
        "exists": path.exists(),
        "is_dir": path.is_dir(),
    }


@router.get("/debug/paths")
def debug_paths():
    vector_db = VectorDBConnector()
    return {
        "project_root": _path_info(PROJECT_ROOT),
        "ingestion_dir": _path_info(SEED_DIR),
        "vector_db_path": _path_info(Path(vector_db.db_path)),
        "cwd": str(Path.cwd()),
    }


@router.get("/debug/seeds")
def debug_seed_files():
    try:
        seed_files = [
            {"name": f.name, "size": f.stat().st_size}
            for f in sorted(SEED_DIR.glob("*.txt"))
        ]
        return {"count": len(seed_files), "files": seed_files}
    except Exception as exc:  # pragma: no cover - defensive
        logger.log_error(f"Failed to list seed files: {exc}")
        return {"count": 0, "files": [], "error": "Unable to read seed directory"}


@router.get("/debug/vector-store")
def debug_vector_store():
    try:
        connector = VectorDBConnector()
        return {
            "vector_count": len(connector.vectors),
            "sample": connector.vectors[:3],
        }
    except Exception as exc:  # pragma: no cover - defensive
        logger.log_error(f"Failed to inspect vector store: {exc}")
        return {"vector_count": 0, "sample": [], "error": "Unable to read vector store"}
