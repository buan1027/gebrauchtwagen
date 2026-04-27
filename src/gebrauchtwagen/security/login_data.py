"""Login-Daten fuer den Token-Abruf."""

from dataclasses import dataclass

__all__ = ["LoginData"]


@dataclass(slots=True)
class LoginData:
    """Benutzername und Passwort fuer den Keycloak-Token-Abruf."""

    username: str
    password: str
