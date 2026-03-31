"""Domänenmodelle für das Aggregat Gebrauchtwagen."""

from gebrauchtwagen.domain.gebrauchtwagen import Gebrauchtwagen
from gebrauchtwagen.domain.hauptuntersuchung import Hauptuntersuchung
from gebrauchtwagen.domain.schaden import Schaden
from gebrauchtwagen.domain.standort import Standort

__all__ = [
    "Gebrauchtwagen",
    "Hauptuntersuchung",
    "Schaden",
    "Standort",
]
