"""Entity fuer Hauptuntersuchungen eines Gebrauchtwagens."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .gebrauchtwagen import Gebrauchtwagen


class Hauptuntersuchung(Base):
    """Historie von Hauptuntersuchungen zu einem Fahrzeug."""

    __tablename__ = "hauptuntersuchung"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    gebrauchtwagen_id: Mapped[int] = mapped_column(
        ForeignKey("gebrauchtwagen.id", ondelete="CASCADE")
    )
    datum: Mapped[date]
    prueforganisation: Mapped[str] = mapped_column(String(100))
    bestanden: Mapped[bool]

    gebrauchtwagen: Mapped[Gebrauchtwagen] = relationship(
        back_populates="hauptuntersuchungen", init=False
    )
