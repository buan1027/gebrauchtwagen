"""Entitätsklasse für den Standort eines Gebrauchtwagens."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Standort:
    """Repräsentiert den physischen Standort eines Gebrauchtwagens."""

    strasse: str
    hausnummer: str
    postleitzahl: str
    stadt: str
