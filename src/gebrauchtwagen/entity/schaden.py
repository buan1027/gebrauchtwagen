"""Entity fuer Schaeden an einem Gebrauchtwagen."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .gebrauchtwagen import Gebrauchtwagen


class Schaden(Base):
    """Dokumentierter Schaden am Fahrzeug."""

    __tablename__ = "schaden"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    gebrauchtwagen_id: Mapped[int] = mapped_column(
        ForeignKey("gebrauchtwagen.id", ondelete="CASCADE")
    )
    bezeichnung: Mapped[str] = mapped_column(String(100))
    beschreibung: Mapped[str] = mapped_column(String(500))
    feststellungsdatum: Mapped[date]

    gebrauchtwagen: Mapped[Gebrauchtwagen] = relationship(
        back_populates="schaeden", init=False
    )
