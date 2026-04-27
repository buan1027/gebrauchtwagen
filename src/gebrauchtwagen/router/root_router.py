"""Router fuer den Root-Endpunkt."""

from typing import Final

from fastapi import APIRouter

__all__ = ["router"]

router: Final = APIRouter(tags=["Root"])


@router.get("/")
def hello() -> dict[str, str]:
    """Liefere eine einfache Begruessung."""
    return {"message": "Hello World"}
