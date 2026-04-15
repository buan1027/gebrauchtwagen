"""Entity-Klassen für die Domäne gebrauchtwagen."""

from .base import Base
from .gebrauchtwagen import Gebrauchtwagen
from .hauptuntersuchung import Hauptuntersuchung
from .schaden import Schaden
from .standort import Standort

__all__ = [
    "Base",
    "Gebrauchtwagen",
    "Hauptuntersuchung",
    "Schaden",
    "Standort",
]
