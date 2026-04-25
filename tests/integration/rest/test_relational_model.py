"""Integrationstest fuer das relationale Modell in PostgreSQL."""

from sqlalchemy import inspect

from gebrauchtwagen.config.db import engine
from gebrauchtwagen.entity import DB_SCHEMA


def test_relational_model_contains_aggregate_relationships() -> None:
    inspector = inspect(engine)

    assert DB_SCHEMA in inspector.get_schema_names()

    table_names = set(inspector.get_table_names(schema=DB_SCHEMA))
    assert {"gebrauchtwagen", "standort", "schaden", "hauptuntersuchung"}.issubset(
        table_names
    )

    gebrauchtwagen_columns = {
        column["name"]
        for column in inspector.get_columns("gebrauchtwagen", schema=DB_SCHEMA)
    }
    standort_columns = {
        column["name"] for column in inspector.get_columns("standort", schema=DB_SCHEMA)
    }
    schaden_columns = {
        column["name"] for column in inspector.get_columns("schaden", schema=DB_SCHEMA)
    }
    hauptuntersuchung_columns = {
        column["name"]
        for column in inspector.get_columns("hauptuntersuchung", schema=DB_SCHEMA)
    }

    assert {
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
    }.issubset(gebrauchtwagen_columns)
    assert {"id", "plz", "ort", "gebrauchtwagen_id"}.issubset(standort_columns)
    assert {
        "id",
        "bezeichnung",
        "beschreibung",
        "feststellungsdatum",
        "gebrauchtwagen_id",
    }.issubset(schaden_columns)
    assert {
        "id",
        "pruefdatum",
        "gueltig_bis",
        "prueforganisation",
        "status",
        "gebrauchtwagen_id",
    }.issubset(hauptuntersuchung_columns)

    standort_fk = {
        fk["referred_table"]
        for fk in inspector.get_foreign_keys("standort", schema=DB_SCHEMA)
        if fk["referred_schema"] == DB_SCHEMA
    }
    schaden_fk = {
        fk["referred_table"]
        for fk in inspector.get_foreign_keys("schaden", schema=DB_SCHEMA)
        if fk["referred_schema"] == DB_SCHEMA
    }
    hauptuntersuchung_fk = {
        fk["referred_table"]
        for fk in inspector.get_foreign_keys("hauptuntersuchung", schema=DB_SCHEMA)
        if fk["referred_schema"] == DB_SCHEMA
    }

    assert standort_fk == {"gebrauchtwagen"}
    assert schaden_fk == {"gebrauchtwagen"}
    assert hauptuntersuchung_fk == {"gebrauchtwagen"}

    standort_unique = {
        tuple(unique_constraint["column_names"])
        for unique_constraint in inspector.get_unique_constraints(
            "standort", schema=DB_SCHEMA
        )
    }
    schaden_unique = {
        tuple(unique_constraint["column_names"])
        for unique_constraint in inspector.get_unique_constraints(
            "schaden", schema=DB_SCHEMA
        )
    }
    hauptuntersuchung_unique = {
        tuple(unique_constraint["column_names"])
        for unique_constraint in inspector.get_unique_constraints(
            "hauptuntersuchung", schema=DB_SCHEMA
        )
    }

    assert ("gebrauchtwagen_id",) in standort_unique
    assert ("gebrauchtwagen_id",) not in schaden_unique
    assert ("gebrauchtwagen_id",) in hauptuntersuchung_unique
