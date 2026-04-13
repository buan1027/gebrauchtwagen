"""Gemeinsame Fixtures fuer Integrationstests."""

import pytest
from sqlalchemy import text

from gebrauchtwagen.config.db import (
    check_database_connection,
    create_tables,
    drop_tables,
    get_session,
)


@pytest.fixture(autouse=True)
def reset_database() -> None:
    """Setze die Datenbank vor jedem Integrationstest zurueck."""
    check_database_connection()
    drop_tables()
    create_tables()
