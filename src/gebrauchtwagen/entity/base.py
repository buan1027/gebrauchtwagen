"""Basisklasse für Entity-Klassen."""

from __future__ import annotations

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

DB_SCHEMA = "gebrauchtwagen"


class Base(MappedAsDataclass, DeclarativeBase):
    """Gemeinsame ORM-Basis für alle Entities."""

    metadata = MetaData(schema=DB_SCHEMA)
