"""Optionale Beispielbefuellung fuer die Datenbank."""

from __future__ import annotations

import csv
import json
import os
from datetime import date
from pathlib import Path
from typing import Any

from sqlalchemy import select

from gebrauchtwagen.config.db import get_session
from gebrauchtwagen.entity import Gebrauchtwagen
from gebrauchtwagen.entity.enums import Fahrzeugklasse, Kraftstoffart

SEED_CSV_ENV = "GEBRAUCHTWAGEN_SEED_CSV"


def seed_database_from_environment() -> None:
    """Lade Beispieldaten, wenn ein CSV-Pfad konfiguriert ist."""
    csv_path = os.environ.get(SEED_CSV_ENV)
    if not csv_path:
        return

    seed_database_from_csv(Path(csv_path))


def seed_database_from_csv(csv_path: Path) -> None:
    """Lade Gebrauchtwagen aus einer CSV-Datei idempotent in die Datenbank."""
    if not csv_path.is_file():
        raise FileNotFoundError(csv_path)

    with csv_path.open(encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")
        entities = [_entity_from_row(row) for row in reader]

    if not entities:
        return

    with get_session() as session:
        existing_fins = set(
            session.scalars(
                select(Gebrauchtwagen.fin).where(
                    Gebrauchtwagen.fin.in_([entity.fin for entity in entities])
                )
            )
        )
        session.add_all(
            entity for entity in entities if entity.fin not in existing_fins
        )
        session.commit()


def _entity_from_row(row: dict[str, str]) -> Gebrauchtwagen:
    ausstattung: dict[str, Any] = (
        json.loads(row["ausstattung"]) if row["ausstattung"] else {}
    )
    beschreibung_url = row["beschreibung_url"] or None

    return Gebrauchtwagen(
        fin=row["fin"],
        marke=row["marke"],
        modell=row["modell"],
        baujahr=int(row["baujahr"]),
        kilometerstand=int(row["kilometerstand"]),
        kraftstoffart=Kraftstoffart(row["kraftstoffart"]),
        fahrzeugklasse=Fahrzeugklasse(row["fahrzeugklasse"]),
        ausstattung=ausstattung,
        erstzulassung=date.fromisoformat(row["erstzulassung"]),
        schadenfrei=row["schadenfrei"].lower() == "true",
        beschreibung_url=beschreibung_url,
    )
