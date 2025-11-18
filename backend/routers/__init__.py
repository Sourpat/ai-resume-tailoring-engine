"""Expose all available API routers for the FastAPI application."""

# Import each router module so it can be referenced explicitly from
# ``backend.routers`` using fully-qualified imports. This ensures Render loads
# the correct modules regardless of the working directory.
from . import admin, debug, debug_ingest, export, tailor, test_routes, upload

__all__ = [
    "admin",
    "debug",
    "debug_ingest",
    "export",
    "tailor",
    "test_routes",
    "upload",
]
