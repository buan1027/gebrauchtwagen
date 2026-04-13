"""DTOs fuer Gebrauchtwagen."""

from __future__ import annotations

from datetime import date, datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

NonEmptyText = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=100),
]

FinText = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=17),
]


class GebrauchtwagenRequestDTO(BaseModel):
    """Request-DTO fuer einen neuen Gebrauchtwagen."""

    model_config = ConfigDict(extra="forbid")

    fin: FinText
    marke: NonEmptyText
    modell: NonEmptyText
    baujahr: int = Field(ge=1900, le=date.today().year)
    kilometerstand: int = Field(ge=0)
    erstzulassung: date
    schadenfrei: bool
    beschreibung_url: str | None = None

    @field_validator("fin", "marke", "modell")
    @classmethod
    def validate_text(cls, value: str) -> str:
        """Validiere nichtleere Textfelder."""
        if not value:
            raise ValueError("darf nicht leer sein")
        return value


class GebrauchtwagenResponseDTO(BaseModel):
    """Response-DTO fuer einen gespeicherten Gebrauchtwagen."""

    model_config = ConfigDict(extra="forbid", from_attributes=True)

    id: int = Field(gt=0)
    version: int = Field(ge=1)
    fin: str
    marke: str
    modell: str
    baujahr: int
    kilometerstand: int
    erstzulassung: date
    schadenfrei: bool
    beschreibung_url: str | None
    erzeugt: datetime
    aktualisiert: datetime
