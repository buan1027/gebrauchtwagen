from fastapi import FastAPI

from gebrauchtwagen.config.db import check_database_connection

app = FastAPI(title="gebrauchtwagen")


@app.on_event("startup")
def startup() -> None:
    check_database_connection()


@app.get("/")
def hello() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "database": "connected"}
