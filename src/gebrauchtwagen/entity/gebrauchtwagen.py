"""Entity-Klasse fuer einen Gebrauchtwagen."""

from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SAEnum
from sqlalchemy import String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import Fahrzeugklasse, Kraftstoffart

if TYPE_CHECKING:
    from .hauptuntersuchung import Hauptuntersuchung
    from .schaden import Schaden
    from .standort import Standort


class Gebrauchtwagen(Base):
    """Entity-Klasse fuer einen Gebrauchtwagen."""

    __tablename__ = "gebrauchtwagen"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    fin: Mapped[str] = mapped_column(String(17), unique=True)
    marke: Mapped[str] = mapped_column(String(100))
    modell: Mapped[str] = mapped_column(String(100))
    baujahr: Mapped[int]
    kilometerstand: Mapped[int]
    kraftstoffart: Mapped[Kraftstoffart] = mapped_column(
        SAEnum(Kraftstoffart, name="kraftstoffart")
    )
    fahrzeugklasse: Mapped[Fahrzeugklasse] = mapped_column(
        SAEnum(Fahrzeugklasse, name="fahrzeugklasse")
    )
    erstzulassung: Mapped[date]
    schadenfrei: Mapped[bool]
    ausstattung: Mapped[dict] = mapped_column(JSONB, default_factory=dict)
    beschreibung_url: Mapped[str | None] = mapped_column(String(255), default=None)
    erzeugt: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    aktualisiert: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    version: Mapped[int] = mapped_column(default=1)

    standort: Mapped[Standort | None] = relationship(
        back_populates="gebrauchtwagen", uselist=False, init=False
    )
    schaeden: Mapped[list[Schaden]] = relationship(
        back_populates="gebrauchtwagen",
        cascade="all, delete-orphan",
        default_factory=list,
        init=False,
    )
    hauptuntersuchungen: Mapped[list[Hauptuntersuchung]] = relationship(
        back_populates="gebrauchtwagen",
        cascade="all, delete-orphan",
        default_factory=list,
        init=False,
    )
