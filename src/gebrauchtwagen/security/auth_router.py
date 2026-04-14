"""REST-Schnittstelle fuer den Keycloak-Token-Abruf."""

from json import JSONDecodeError
from typing import Annotated, Any, Final

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import JSONResponse

from gebrauchtwagen.security.dependencies import get_token_service
from gebrauchtwagen.security.login_data import LoginData
from gebrauchtwagen.security.token_service import TokenService

__all__ = ["router"]

router: Final = APIRouter(prefix="/auth", tags=["Auth"])


async def request_body_to_dict(request: Request) -> dict[str, Any]:
    """Lies den Body ohne Pydantic-422, damit Loginfehler 401 bleiben."""
    try:
        body: dict[str, Any] = await request.json()
        return body
    except JSONDecodeError:
        return {}


@router.post("/token")
def token(
    body: Annotated[dict[str, Any], Depends(request_body_to_dict)],
    service: Annotated[TokenService, Depends(get_token_service)],
) -> Response:
    """Fordere bei Keycloak einen Access Token an."""
    try:
        login_data: Final = LoginData(**body)
    except TypeError:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

    token_response: Final = service.token(
        username=login_data.username,
        password=login_data.password,
    )
    access_token: Final = token_response["access_token"]
    roles: Final = service.get_roles_from_token(token=access_token)

    return JSONResponse(
        content={
            "token": access_token,
            "expires_in": token_response["expires_in"],
            "rollen": roles,
        },
    )
