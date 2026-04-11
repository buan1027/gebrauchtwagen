from contextlib import asynccontextmanager
from typing import Final

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import Response
from starlette.exceptions import HTTPException as StarletteHTTPException

from gebrauchtwagen.config.db import (
    check_database_connection,
    create_tables,
    engine,
)
from gebrauchtwagen.graphql_api import graphql_router
from gebrauchtwagen.problem_details import create_problem_details
from gebrauchtwagen.router.gebrauchtwagen_router import router as gebrauchtwagen_router
from gebrauchtwagen.router.health_router import router as health_router
from gebrauchtwagen.router.root_router import router as root_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Beim Start DB pruefen und Tabellen erzeugen, beim Ende Engine freigeben."""
    check_database_connection()
    create_tables()
    yield
    engine.dispose()


app: Final = FastAPI(title="gebrauchtwagen", lifespan=lifespan)
app.include_router(root_router)
app.include_router(health_router)
app.include_router(gebrauchtwagen_router)
app.include_router(graphql_router, prefix="/graphql")


@app.exception_handler(StarletteHTTPException)
def http_exception_handler(_request: Request, err: StarletteHTTPException) -> Response:
    """Einheitliche Fehlerantwort fuer HTTP-Fehler."""
    if err.status_code == status.HTTP_404_NOT_FOUND:
        return create_problem_details(
            status_code=err.status_code,
            detail=f"Der Pfad wurde nicht gefunden: {_request.url.path}",
        )
    return create_problem_details(status_code=err.status_code, detail=err.detail)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(
    _request: Request,
    err: RequestValidationError,
) -> Response:
    """Einheitliche Fehlerantwort fuer Validierungsfehler."""
    return create_problem_details(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        detail=err.errors(),
    )
