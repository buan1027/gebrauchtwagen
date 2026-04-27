"""Rollenpruefung fuer FastAPI-Dependencies."""

from typing import Annotated, Final

from fastapi import Depends, HTTPException, Request, status

from gebrauchtwagen.security.dependencies import get_token_service
from gebrauchtwagen.security.role import Role
from gebrauchtwagen.security.token_service import TokenService
from gebrauchtwagen.security.user import User

__all__ = ["RolesRequired"]


class RolesRequired:
    """Pruefe, ob der aktuelle Benutzer eine der benoetigten Rollen hat."""

    def __init__(self, required_roles: list[Role] | Role) -> None:
        """Speichere die benoetigten Rollen."""
        self.required_roles = required_roles

    def __call__(
        self,
        request: Request,
        service: Annotated[TokenService, Depends(get_token_service)],
    ) -> None:
        """Pruefe die Rollen des aktuellen Requests."""
        user: Final[User] = service.get_user_from_request(request)
        required_roles = (
            [self.required_roles]
            if isinstance(self.required_roles, Role)
            else self.required_roles
        )
        if any(role in required_roles for role in user.roles):
            request.state.current_user = user
            return
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
