"""GraphQL-Typen fuer Gebrauchtwagen."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, cast

import strawberry

from gebrauchtwagen.entity.dto import GebrauchtwagenResponseDTO
from gebrauchtwagen.entity.enums import Fahrzeugklasse, Kraftstoffart

__all__ = ["Gebrauchtwagen"]

KraftstoffartGQL = strawberry.enum(Kraftstoffart)
FahrzeugklasseGQL = strawberry.enum(Fahrzeugklasse)


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
    kraftstoffart: KraftstoffartGQL
    fahrzeugklasse: FahrzeugklasseGQL
    ausstattung: strawberry.scalars.JSON
    erstzulassung: date
    schadenfrei: bool
    beschreibung_url: str | None
    erzeugt: datetime
    aktualisiert: datetime

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
            kraftstoffart=KraftstoffartGQL(dto.kraftstoffart.value),
            fahrzeugklasse=FahrzeugklasseGQL(dto.fahrzeugklasse.value),
            ausstattung=cast("strawberry.scalars.JSON", dto.ausstattung),
            erstzulassung=dto.erstzulassung,
            schadenfrei=dto.schadenfrei,
            beschreibung_url=dto.beschreibung_url,
            erzeugt=dto.erzeugt,
            aktualisiert=dto.aktualisiert,
        )
