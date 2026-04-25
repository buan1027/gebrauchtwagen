"""Entity fuer die Hauptuntersuchung eines Gebrauchtwagens."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import HuStatus

if TYPE_CHECKING:
    from .gebrauchtwagen import Gebrauchtwagen


class Hauptuntersuchung(Base):
    """Hauptuntersuchung zu einem Fahrzeug."""

    __tablename__ = "hauptuntersuchung"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    gebrauchtwagen_id: Mapped[int] = mapped_column(
        ForeignKey("gebrauchtwagen.id", ondelete="CASCADE"),
        unique=True,
    )
    pruefdatum: Mapped[date]
    gueltig_bis: Mapped[date]
    prueforganisation: Mapped[str] = mapped_column(String(100))
    status: Mapped[HuStatus] = mapped_column(
        SAEnum(HuStatus, name="hu_status")
    )

    gebrauchtwagen: Mapped[Gebrauchtwagen] = relationship(
        back_populates="hauptuntersuchung", init=False
    )
