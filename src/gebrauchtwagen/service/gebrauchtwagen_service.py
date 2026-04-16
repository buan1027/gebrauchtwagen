"""Geschaeftslogik fuer Gebrauchtwagen."""

from __future__ import annotations

from fastapi import HTTPException, status

from gebrauchtwagen.entity import Gebrauchtwagen
from gebrauchtwagen.entity.dto import (
    GebrauchtwagenRequestDTO,
    GebrauchtwagenResponseDTO,
)
from gebrauchtwagen.repository import gebrauchtwagen_repository

__all__ = ["create_gebrauchtwagen", "get_gebrauchtwagen_by_id", "list_gebrauchtwagen"]


def list_gebrauchtwagen() -> list[GebrauchtwagenResponseDTO]:
    """Lies alle Gebrauchtwagen als Response-DTOs."""
    gebrauchtwagen_list = gebrauchtwagen_repository.find_all()
    return [
        GebrauchtwagenResponseDTO.model_validate(item) for item in gebrauchtwagen_list
    ]


def get_gebrauchtwagen_by_id(gebrauchtwagen_id: int) -> GebrauchtwagenResponseDTO:
    """Lies einen Gebrauchtwagen anhand seiner ID."""
    gebrauchtwagen = gebrauchtwagen_repository.find_by_id(gebrauchtwagen_id)
    if gebrauchtwagen is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gebrauchtwagen mit ID {gebrauchtwagen_id} nicht gefunden.",
        )
    return GebrauchtwagenResponseDTO.model_validate(gebrauchtwagen)


def create_gebrauchtwagen(
    request: GebrauchtwagenRequestDTO,
) -> GebrauchtwagenResponseDTO:
    """Erzeuge einen Gebrauchtwagen aus dem Request-DTO."""
    entity = Gebrauchtwagen(**request.model_dump())
    saved_entity = gebrauchtwagen_repository.create(entity)
    return GebrauchtwagenResponseDTO.model_validate(saved_entity)
