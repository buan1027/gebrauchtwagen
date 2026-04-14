"""REST-Router fuer Gebrauchtwagen."""

from typing import Final

from fastapi import APIRouter, Depends, status

from gebrauchtwagen.entity.dto import (
    GebrauchtwagenRequestDTO,
    GebrauchtwagenResponseDTO,
)
from gebrauchtwagen.security import Role, RolesRequired
from gebrauchtwagen.service import gebrauchtwagen_service

__all__ = ["router"]

router: Final = APIRouter(prefix="/gebrauchtwagen", tags=["Gebrauchtwagen"])


@router.get("", response_model=list[GebrauchtwagenResponseDTO])
def list_gebrauchtwagen() -> list[GebrauchtwagenResponseDTO]:
    """Liefere alle Gebrauchtwagen."""
    return gebrauchtwagen_service.list_gebrauchtwagen()


@router.post(
    "",
    dependencies=[Depends(RolesRequired(Role.ADMIN))],
    response_model=GebrauchtwagenResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
def create_gebrauchtwagen(
    request: GebrauchtwagenRequestDTO,
) -> GebrauchtwagenResponseDTO:
    """Lege einen Gebrauchtwagen an."""
    return gebrauchtwagen_service.create_gebrauchtwagen(request)
