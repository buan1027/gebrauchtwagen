"""Liest die Anwendungskonfiguration aus TOML."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib


@dataclass(slots=True)
class ServerSettings:
    host: str
    port: int


@dataclass(slots=True)
class TlsSettings:
    certfile: Path
    keyfile: Path


@dataclass(slots=True)
class Settings:
    server: ServerSettings
    tls: TlsSettings


def load_settings() -> Settings:
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
    )
