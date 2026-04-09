from fastapi import FastAPI, status

from gebrauchtwagen.config.db import (
    check_database_connection,
    create_tables,
    is_database_connected,
)
from gebrauchtwagen.entity.dto import (
    GebrauchtwagenRequestDTO,
    GebrauchtwagenResponseDTO,
)

app = FastAPI(title="gebrauchtwagen")
_gebrauchtwagen_store: list[GebrauchtwagenResponseDTO] = []


@app.on_event("startup")
def startup() -> None:
    check_database_connection()
    create_tables()


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
    return _gebrauchtwagen_store


@app.post(
    "/gebrauchtwagen",
    response_model=GebrauchtwagenResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
def create_gebrauchtwagen(
    request: GebrauchtwagenRequestDTO,
) -> GebrauchtwagenResponseDTO:
    created = GebrauchtwagenResponseDTO(
        id=len(_gebrauchtwagen_store) + 1,
        version=1,
        **request.model_dump(),
    )
    _gebrauchtwagen_store.append(created)
    return created
