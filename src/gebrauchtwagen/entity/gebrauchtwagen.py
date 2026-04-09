"""Entity-Klasse fuer einen Gebrauchtwagen."""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Gebrauchtwagen(Base):
    """Entity-Klasse fuer einen Gebrauchtwagen."""

    __tablename__ = "gebrauchtwagen"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    fin: Mapped[str] = mapped_column(String(17), unique=True)
    marke: Mapped[str] = mapped_column(String(100))
    modell: Mapped[str] = mapped_column(String(100))
    baujahr: Mapped[int]
    kilometerstand: Mapped[int]
    version: Mapped[int] = mapped_column(default=1)
