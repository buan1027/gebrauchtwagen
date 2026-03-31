"""Entitätsklasse für einen Schaden an einem Gebrauchtwagen."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Schaden:
    """Repräsentiert einen Schaden an einem Gebrauchtwagen."""

    beschreibung: str
    repariert: bool
