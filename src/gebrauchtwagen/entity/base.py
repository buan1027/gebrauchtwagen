"""Basisklasse für Entity-Klassen."""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(MappedAsDataclass, DeclarativeBase):
    """Gemeinsame ORM-Basis für alle Entities."""
