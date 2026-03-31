"""Entitätsklasse für die Hauptuntersuchung eines Gebrauchtwagens."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class Hauptuntersuchung:
    """Repräsentiert eine Hauptuntersuchung (HU/TÜV) eines Gebrauchtwagens."""

    datum: date
    bestanden: bool
    naechste_faelligkeit: date
