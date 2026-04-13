"""Entity-Klasse fuer einen Gebrauchtwagen."""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import String, func
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
    erstzulassung: Mapped[date]
    schadenfrei: Mapped[bool]
    beschreibung_url: Mapped[str | None] = mapped_column(String(255), default=None)
    erzeugt: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    aktualisiert: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    version: Mapped[int] = mapped_column(default=1)
