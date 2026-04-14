"""Benutzerdaten aus einem Keycloak-Token."""

from dataclasses import dataclass

from gebrauchtwagen.security.role import Role

__all__ = ["User"]


@dataclass(slots=True)
class User:
    """Minimaldaten eines authentifizierten Benutzers."""

    username: str
    roles: list[Role]
