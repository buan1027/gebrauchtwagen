from __future__ import annotations

from datetime import date
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
    model_config = ConfigDict(extra="forbid")

    fin: FinText
    marke: NonEmptyText
    modell: NonEmptyText
    baujahr: int = Field(ge=1900, le=date.today().year)
    kilometerstand: int = Field(ge=0)

    @field_validator("fin", "marke", "modell")
    @classmethod
    def validate_text(cls, value: str) -> str:
        if not value:
            raise ValueError("darf nicht leer sein")
        return value


class GebrauchtwagenResponseDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    id: int = Field(gt=0)
    version: int = Field(ge=1)
    fin: str
    marke: str
    modell: str
    baujahr: int
    kilometerstand: int
