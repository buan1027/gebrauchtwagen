"""Geschaeftslogik fuer Gebrauchtwagen."""

from __future__ import annotations

from gebrauchtwagen.entity import Gebrauchtwagen
from gebrauchtwagen.entity.dto import (
    GebrauchtwagenRequestDTO,
    GebrauchtwagenResponseDTO,
)
from gebrauchtwagen.repository import gebrauchtwagen_repository

__all__ = ["create_gebrauchtwagen", "list_gebrauchtwagen"]


def list_gebrauchtwagen() -> list[GebrauchtwagenResponseDTO]:
    """Lies alle Gebrauchtwagen als Response-DTOs."""
    gebrauchtwagen_list = gebrauchtwagen_repository.find_all()
    return [
        GebrauchtwagenResponseDTO.model_validate(item) for item in gebrauchtwagen_list
    ]


def create_gebrauchtwagen(
    request: GebrauchtwagenRequestDTO,
) -> GebrauchtwagenResponseDTO:
    """Erzeuge einen Gebrauchtwagen aus dem Request-DTO."""
    entity = Gebrauchtwagen(**request.model_dump())
    saved_entity = gebrauchtwagen_repository.create(entity)
    return GebrauchtwagenResponseDTO.model_validate(saved_entity)
