"""Gemeinsame Fixtures fuer Integrationstests."""

import pytest
from fastapi import HTTPException, status

from gebrauchtwagen.config.db import (
    check_database_connection,
    create_tables,
    drop_tables,
)
from gebrauchtwagen.security.dependencies import get_token_service
from gebrauchtwagen.security.role import Role
from gebrauchtwagen.security.user import User


@pytest.fixture(autouse=True)
def reset_database() -> None:
    """Setze die Datenbank vor jedem Integrationstest zurueck."""
    check_database_connection()
    drop_tables()
    create_tables()


@pytest.fixture(autouse=True)
def accept_integration_test_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """Akzeptiere einen lokalen Test-Token ohne Keycloak-Netzwerkzugriff."""

    def get_user_from_token(token: str) -> User:
        if token == "integration-test-token":  # noqa: S105
            return User(username="integration-test", roles=[Role.ADMIN])
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    monkeypatch.setattr(
        get_token_service(),
        "get_user_from_token",
        get_user_from_token,
    )
