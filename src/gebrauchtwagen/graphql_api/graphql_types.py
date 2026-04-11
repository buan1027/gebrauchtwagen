"""GraphQL-Typen fuer Gebrauchtwagen."""

from __future__ import annotations

import strawberry

from gebrauchtwagen.entity.dto import GebrauchtwagenResponseDTO

__all__ = ["Gebrauchtwagen"]


@strawberry.type
class Gebrauchtwagen:
    """GraphQL-Typ fuer einen Gebrauchtwagen."""

    id: int
    version: int
    fin: str
    marke: str
    modell: str
    baujahr: int
    kilometerstand: int

    @classmethod
    def from_dto(cls, dto: GebrauchtwagenResponseDTO) -> Gebrauchtwagen:
        """Erzeuge den GraphQL-Typ aus einem Response-DTO."""
        return cls(
            id=dto.id,
            version=dto.version,
            fin=dto.fin,
            marke=dto.marke,
            modell=dto.modell,
            baujahr=dto.baujahr,
            kilometerstand=dto.kilometerstand,
        )
