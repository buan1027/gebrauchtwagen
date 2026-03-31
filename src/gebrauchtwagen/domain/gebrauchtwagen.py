"""Entitätsklasse für das Aggregat Gebrauchtwagen."""

from __future__ import annotations

from dataclasses import dataclass, field

from gebrauchtwagen.domain.hauptuntersuchung import Hauptuntersuchung
from gebrauchtwagen.domain.schaden import Schaden
from gebrauchtwagen.domain.standort import Standort


@dataclass(slots=True)
class Gebrauchtwagen:
    """Repräsentiert einen Gebrauchtwagen als zentrales Aggregat."""

    marke: str
    modell: str
    baujahr: int
    kilometerstand: int
    standort: Standort
    schaeden: list[Schaden] = field(default_factory=list)
    hauptuntersuchungen: list[Hauptuntersuchung] = field(default_factory=list)
