"""Datenbankzugriff fuer Gebrauchtwagen."""

from __future__ import annotations

from sqlalchemy import select

from gebrauchtwagen.config.db import get_session
from gebrauchtwagen.entity import Gebrauchtwagen

__all__ = ["create", "find_all"]


def find_all() -> list[Gebrauchtwagen]:
    """Lies alle Gebrauchtwagen sortiert nach ID."""
    with get_session() as session:
        return list(
            session.scalars(select(Gebrauchtwagen).order_by(Gebrauchtwagen.id)).all()
        )


def create(gebrauchtwagen: Gebrauchtwagen) -> Gebrauchtwagen:
    """Speichere einen Gebrauchtwagen und liefere den persistierten Stand."""
    with get_session() as session:
        session.add(gebrauchtwagen)
        session.commit()
        session.refresh(gebrauchtwagen)
        return gebrauchtwagen
