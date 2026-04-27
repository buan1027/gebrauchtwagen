"""Startpunkt fuer die Gebrauchtwagen-Anwendung."""

from __future__ import annotations

from pathlib import Path

import uvicorn

from gebrauchtwagen.config.settings import load_settings


def _existing_config_path(project_root: Path, path: Path) -> Path | None:
    """Liefere einen vorhandenen Konfigurationspfad, falls er existiert."""
    candidate = path if path.is_absolute() else project_root / path
    if candidate.exists():
        return candidate
    return None


def main() -> None:
    """Run the application with Uvicorn."""
    settings = load_settings()
    project_root = Path(__file__).resolve().parents[2]
    certfile = _existing_config_path(project_root, settings.tls.certfile)
    keyfile = _existing_config_path(project_root, settings.tls.keyfile)

    if certfile is not None and keyfile is not None:
        uvicorn.run(
            "gebrauchtwagen.main:app",
            host=settings.server.host,
            port=settings.server.port,
            ssl_certfile=str(certfile),
            ssl_keyfile=str(keyfile),
        )
        return

    uvicorn.run(
        "gebrauchtwagen.main:app",
        host=settings.server.host,
        port=settings.server.port,
    )


if __name__ == "__main__":
    main()
