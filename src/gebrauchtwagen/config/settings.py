"""Liest die Anwendungskonfiguration aus TOML."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ServerSettings:
    """Server-Konfiguration."""

    host: str
    port: int


@dataclass(slots=True)
class TlsSettings:
    """TLS-Konfiguration."""

    certfile: Path
    keyfile: Path


@dataclass(slots=True)
class DbSettings:
    """Datenbank-Konfiguration."""

    host: str
    port: int
    name: str
    username: str
    password: str
    echo: bool


@dataclass(slots=True)
class Settings:
    """Gesamte Anwendungskonfiguration."""

    server: ServerSettings
    tls: TlsSettings
    db: DbSettings


def load_settings() -> Settings:
    """Lies die Anwendungskonfiguration aus der TOML-Datei."""
    config_path = Path(__file__).with_name("application.toml")
    data = tomllib.loads(config_path.read_text(encoding="utf-8"))

    return Settings(
        server=ServerSettings(
            host=data["server"]["host"],
            port=data["server"]["port"],
        ),
        tls=TlsSettings(
            certfile=Path(data["tls"]["certfile"]),
            keyfile=Path(data["tls"]["keyfile"]),
        ),
        db=DbSettings(
            host=data["db"]["host"],
            port=data["db"]["port"],
            name=data["db"]["name"],
            username=data["db"]["username"],
            password=data["db"]["password"],
            echo=data["db"]["echo"],
        ),
    )
