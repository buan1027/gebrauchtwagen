"""Integrationstest fuer die optionale CSV-Beispielbefuellung."""

from pathlib import Path

from gebrauchtwagen.config.seed import seed_database_from_csv
from gebrauchtwagen.repository.gebrauchtwagen_repository import find_all


def test_seed_database_from_csv_is_idempotent() -> None:
    seed_path = Path("extras/compose/gebrauchtwagen/gebrauchtwagen.csv")

    seed_database_from_csv(seed_path)
    seed_database_from_csv(seed_path)

    items = find_all()
    assert len(items) == 3
    assert [item.fin for item in items] == [
        "WVWZZZ1JZXW100001",
        "WBA8E31050K100002",
        "WME4533911K100003",
    ]
