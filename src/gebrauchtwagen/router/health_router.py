"""Router fuer Health-Endpunkte."""

from typing import Final

from fastapi import APIRouter

from gebrauchtwagen.config.db import is_database_connected

__all__ = ["router"]

router: Final = APIRouter(tags=["Health"])


@router.get("/health")
def health() -> dict[str, str]:
    """Liefere den Health-Status der Anwendung."""
    if is_database_connected():
        return {"status": "ok", "database": "connected"}

    return {"status": "degraded", "database": "disconnected"}
