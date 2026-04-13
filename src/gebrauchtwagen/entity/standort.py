"""Entity fuer den Standort eines Gebrauchtwagens."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
	from .gebrauchtwagen import Gebrauchtwagen


class Standort(Base):
	"""Standort, an dem ein Gebrauchtwagen angeboten wird."""

	__tablename__ = "standort"

	id: Mapped[int] = mapped_column(init=False, primary_key=True)
	gebrauchtwagen_id: Mapped[int] = mapped_column(
		ForeignKey("gebrauchtwagen.id", ondelete="CASCADE"),
		unique=True,
	)
	name: Mapped[str] = mapped_column(String(100))
	stadt: Mapped[str] = mapped_column(String(100))

	gebrauchtwagen: Mapped[Gebrauchtwagen] = relationship(
		back_populates="standort", init=False
	)
