from contextlib import asynccontextmanager
from typing import Final

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import Response
from sqlalchemy import select
from starlette.exceptions import HTTPException as StarletteHTTPException

from gebrauchtwagen.config.db import (
    check_database_connection,
    create_tables,
    engine,
    get_session,
    is_database_connected,
)
from gebrauchtwagen.entity import Gebrauchtwagen
from gebrauchtwagen.entity.dto import (
    GebrauchtwagenRequestDTO,
    GebrauchtwagenResponseDTO,
)
from gebrauchtwagen.problem_details import create_problem_details


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Beim Start DB pruefen und Tabellen erzeugen, beim Ende Engine freigeben."""
    check_database_connection()
    create_tables()
    yield
    engine.dispose()


app: Final = FastAPI(title="gebrauchtwagen", lifespan=lifespan)


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


@app.get("/")
def hello() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/health")
def health() -> dict[str, str]:
    if is_database_connected():
        return {"status": "ok", "database": "connected"}

    return {"status": "degraded", "database": "disconnected"}


@app.get("/gebrauchtwagen", response_model=list[GebrauchtwagenResponseDTO])
def list_gebrauchtwagen() -> list[GebrauchtwagenResponseDTO]:
    with get_session() as session:
        gebrauchtwagen_list = session.scalars(
            select(Gebrauchtwagen).order_by(Gebrauchtwagen.id)
        ).all()
    return [GebrauchtwagenResponseDTO.model_validate(item) for item in gebrauchtwagen_list]


@app.post(
    "/gebrauchtwagen",
    response_model=GebrauchtwagenResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
def create_gebrauchtwagen(
    request: GebrauchtwagenRequestDTO,
) -> GebrauchtwagenResponseDTO:
    entity = Gebrauchtwagen(**request.model_dump())

    with get_session() as session:
        session.add(entity)
        session.commit()
        session.refresh(entity)

    return GebrauchtwagenResponseDTO.model_validate(entity)
