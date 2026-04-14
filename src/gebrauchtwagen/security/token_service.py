"""Token-Service fuer Keycloak."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict
from typing import Any, Final

from fastapi import HTTPException, Request, status
from jwcrypto.common import JWException
from keycloak import KeycloakAuthenticationError, KeycloakOpenID

from gebrauchtwagen.config.settings import load_settings
from gebrauchtwagen.security.role import Role
from gebrauchtwagen.security.user import User

__all__ = ["TokenService"]


class TokenService:
    """Schnittstelle fuer Token-Abruf und Token-Pruefung."""

    def __init__(self) -> None:
        """Initialisiere die Keycloak-OpenID-Schnittstelle."""
        self.keycloak = KeycloakOpenID(**asdict(load_settings().keycloak))

    def token(self, username: str | None, password: str | None) -> Mapping[str, Any]:
        """Fordere bei Keycloak einen Token fuer Benutzername und Passwort an."""
        if username is None or password is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        try:
            return self.keycloak.token(username, password)
        except KeycloakAuthenticationError as err:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from err

    def _get_token_from_request(self, request: Request) -> str:
        """Extrahiere das Bearer Token aus dem Authorization-Header."""
        authorization_header: Final = request.headers.get("Authorization")
        if authorization_header is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        try:
            authorization_scheme, bearer_token = authorization_header.split()
        except ValueError as err:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from err
        if authorization_scheme.lower() != "bearer":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return bearer_token

    def get_user_from_token(self, token: str) -> User:
        """Lies Benutzername und Rollen aus einem Access Token."""
        try:
            token_decoded: Final[Mapping[str, Any]] = self.keycloak.decode_token(
                token=token,
            )
        except JWException as err:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from err

        username = str(token_decoded["preferred_username"])
        roles = self.get_roles_from_token(token_decoded)
        return User(username=username, roles=roles)

    def get_user_from_request(self, request: Request) -> User:
        """Lies den authentifizierten Benutzer aus dem Request."""
        bearer_token = self._get_token_from_request(request)
        return self.get_user_from_token(token=bearer_token)

    def get_roles_from_token(self, token: str | Mapping[str, Any]) -> list[Role]:
        """Lies die Client-Rollen aus einem Keycloak-Token."""
        if isinstance(token, str):
            token_decoded = self.keycloak.decode_token(token=token)
        else:
            token_decoded = token

        client_id = self.keycloak.client_id
        roles: list[str] = token_decoded.get("resource_access", {}).get(
            client_id,
            {},
        ).get("roles", [])
        return [
            Role[role_name]
            for role in roles
            if (role_name := role.upper()) in Role.__members__
        ]
