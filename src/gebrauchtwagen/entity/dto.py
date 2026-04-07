from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

NonEmptyText = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=100),
]


class GebrauchtwagenRequestDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")

    marke: NonEmptyText
    modell: NonEmptyText
    baujahr: int = Field(ge=1900, le=date.today().year)
    kilometerstand: int = Field(ge=0)
    preis_eur: Decimal = Field(gt=0, max_digits=10, decimal_places=2)

    @field_validator("marke", "modell")
    @classmethod
    def validate_text(cls, value: str) -> str:
        if not value:
            raise ValueError("darf nicht leer sein")
        return value


class GebrauchtwagenResponseDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int = Field(gt=0)
    marke: str
    modell: str
    baujahr: int
    kilometerstand: int
    preis_eur: Decimal
    