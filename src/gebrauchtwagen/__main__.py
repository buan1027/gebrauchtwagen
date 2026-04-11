"""Startpunkt fuer die Gebrauchtwagen-Anwendung."""

from __future__ import annotations

from pathlib import Path

import uvicorn

from gebrauchtwagen.config.settings import load_settings


def main() -> None:
    """Run the application with Uvicorn."""
    settings = load_settings()
    project_root = Path(__file__).resolve().parents[2]

    uvicorn.run(
        "gebrauchtwagen.main:app",
        host=settings.server.host,
        port=settings.server.port,
        ssl_certfile=str(project_root / settings.tls.certfile),
        ssl_keyfile=str(project_root / settings.tls.keyfile),
    )


if __name__ == "__main__":
    main()
