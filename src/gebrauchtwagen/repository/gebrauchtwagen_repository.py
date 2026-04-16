"""Datenbankzugriff fuer Gebrauchtwagen."""

from __future__ import annotations

from sqlalchemy import select

from gebrauchtwagen.config.db import get_session
from gebrauchtwagen.entity import Gebrauchtwagen

__all__ = ["create", "find_all", "find_by_id"]


def find_all() -> list[Gebrauchtwagen]:
    """Lies alle Gebrauchtwagen sortiert nach ID."""
    with get_session() as session:
        return list(
            session.scalars(select(Gebrauchtwagen).order_by(Gebrauchtwagen.id)).all()
        )


def find_by_id(gebrauchtwagen_id: int) -> Gebrauchtwagen | None:
    """Lies einen Gebrauchtwagen anhand seiner ID."""
    with get_session() as session:
        return session.get(Gebrauchtwagen, gebrauchtwagen_id)


def create(gebrauchtwagen: Gebrauchtwagen) -> Gebrauchtwagen:
    """Speichere einen Gebrauchtwagen und liefere den persistierten Stand."""
    with get_session() as session:
        session.add(gebrauchtwagen)
        session.commit()
        session.refresh(gebrauchtwagen)
        return gebrauchtwagen
