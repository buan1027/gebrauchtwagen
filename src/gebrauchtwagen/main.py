from fastapi import FastAPI

app = FastAPI(title="gebrauchtwagen")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
