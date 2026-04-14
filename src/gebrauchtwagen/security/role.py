"""Rollen aus dem Keycloak-Client."""

from enum import StrEnum

__all__ = ["Role"]


class Role(StrEnum):
    """Keycloak-Client-Rollen."""

    ADMIN = "ADMIN"
