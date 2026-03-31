from fastapi import FastAPI

app = FastAPI(title="gebrauchtwagen")


@app.get("/")
def hello() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
