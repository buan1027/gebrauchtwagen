"""Tests fuer die PostgreSQL-Initialisierungsdateien."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INIT_DIR = ROOT / "extras" / "compose" / "postgres" / "init" / "gebrauchtwagen"
SQL_DIR = INIT_DIR / "sql"
CSV_DIR = INIT_DIR / "csv"


def test_postgres_init_sql_files_exist() -> None:
    create_db = SQL_DIR / "create-db.sql"
    create_schema = SQL_DIR / "create-schema.sql"
    load_csv = SQL_DIR / "load-csv.sql"

    assert create_db.is_file()
    assert create_schema.is_file()
    assert load_csv.is_file()

    schema_sql = create_schema.read_text(encoding="utf-8")
    assert "CREATE SCHEMA IF NOT EXISTS AUTHORIZATION gebrauchtwagen" in schema_sql
    assert "CREATE TABLE IF NOT EXISTS gebrauchtwagen.gebrauchtwagen" in schema_sql
    assert "CREATE TABLE IF NOT EXISTS gebrauchtwagen.standort" in schema_sql
    assert "CREATE TABLE IF NOT EXISTS gebrauchtwagen.schaden" in schema_sql
    assert "CREATE TABLE IF NOT EXISTS gebrauchtwagen.hauptuntersuchung" in schema_sql

    load_sql = load_csv.read_text(encoding="utf-8")
    assert "COPY gebrauchtwagen (" in load_sql
    assert "COPY standort (" in load_sql
    assert "COPY schaden (" in load_sql
    assert "COPY hauptuntersuchung (" in load_sql


def test_postgres_init_csv_headers_match_target_model() -> None:
    expected_headers = {
        "gebrauchtwagen.csv": [
            "id",
            "version",
            "fin",
            "marke",
            "modell",
            "baujahr",
            "erstzulassung",
            "kilometerstand",
            "kraftstoffart",
            "fahrzeugklasse",
            "ausstattung",
            "schadenfrei",
            "beschreibung_url",
            "anbieter_username",
            "kontakt_email",
            "erzeugt",
            "aktualisiert",
        ],
        "standort.csv": ["id", "plz", "ort", "gebrauchtwagen_id"],
        "schaden.csv": [
            "id",
            "bezeichnung",
            "beschreibung",
            "feststellungsdatum",
            "gebrauchtwagen_id",
        ],
        "hauptuntersuchung.csv": [
            "id",
            "pruefdatum",
            "gueltig_bis",
            "prueforganisation",
            "status",
            "gebrauchtwagen_id",
        ],
    }

    for file_name, expected_header in expected_headers.items():
        with (CSV_DIR / file_name).open(encoding="utf-8", newline="") as csv_file:
            reader = csv.reader(csv_file, delimiter=";")
            assert next(reader) == expected_header
            assert next(reader, None) is not None
