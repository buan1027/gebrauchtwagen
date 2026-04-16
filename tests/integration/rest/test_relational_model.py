"""Integrationstest fuer das relationale Modell in PostgreSQL."""

from sqlalchemy import inspect

from gebrauchtwagen.config.db import engine


def test_relational_model_contains_aggregate_relationships() -> None:
    inspector = inspect(engine)

    table_names = set(inspector.get_table_names())
    assert {"gebrauchtwagen", "standort", "schaden", "hauptuntersuchung"}.issubset(
        table_names
    )

    standort_fk = {
        fk["referred_table"] for fk in inspector.get_foreign_keys("standort")
    }
    schaden_fk = {fk["referred_table"] for fk in inspector.get_foreign_keys("schaden")}
    hauptuntersuchung_fk = {
        fk["referred_table"] for fk in inspector.get_foreign_keys("hauptuntersuchung")
    }

    assert standort_fk == {"gebrauchtwagen"}
    assert schaden_fk == {"gebrauchtwagen"}
    assert hauptuntersuchung_fk == {"gebrauchtwagen"}

    standort_unique = {
        tuple(unique_constraint["column_names"])
        for unique_constraint in inspector.get_unique_constraints("standort")
    }
    schaden_unique = {
        tuple(unique_constraint["column_names"])
        for unique_constraint in inspector.get_unique_constraints("schaden")
    }
    hauptuntersuchung_unique = {
        tuple(unique_constraint["column_names"])
        for unique_constraint in inspector.get_unique_constraints("hauptuntersuchung")
    }

    assert ("gebrauchtwagen_id",) in standort_unique
    assert ("gebrauchtwagen_id",) not in schaden_unique
    assert ("gebrauchtwagen_id",) in hauptuntersuchung_unique
