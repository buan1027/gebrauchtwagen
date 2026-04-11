"""Liest die Anwendungskonfiguration aus TOML."""

from __future__ import annotations

import tomllib
from collections.abc import Mapping
from dataclasses import dataclass
from os import environ
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


def _get_env(name: str) -> str | None:
    """Lies eine projektspezifische Umgebungsvariable."""
    return environ.get(f"GEBRAUCHTWAGEN_{name}")


def _get_int_env(name: str, default: int) -> int:
    """Lies eine Integer-Umgebungsvariable mit Fallback."""
    value = _get_env(name)
    if value is None:
        return default
    return int(value)


def _get_bool_env(name: str, *, default: bool) -> bool:
    """Lies eine Boolean-Umgebungsvariable mit Fallback."""
    value = _get_env(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def _get_path_env(name: str, default: str) -> Path:
    """Lies eine Pfad-Umgebungsvariable mit Fallback."""
    return Path(_get_env(name) or default)


def load_settings() -> Settings:
    """Lies die Anwendungskonfiguration aus der TOML-Datei."""
    config_path = Path(__file__).with_name("application.toml")
    data = tomllib.loads(config_path.read_text(encoding="utf-8"))
    server: Mapping[str, str | int] = data["server"]
    tls: Mapping[str, str] = data["tls"]
    db: Mapping[str, str | int | bool] = data["db"]

    return Settings(
        server=ServerSettings(
            host=_get_env("SERVER_HOST") or str(server["host"]),
            port=_get_int_env("SERVER_PORT", int(server["port"])),
        ),
        tls=TlsSettings(
            certfile=_get_path_env("TLS_CERTFILE", tls["certfile"]),
            keyfile=_get_path_env("TLS_KEYFILE", tls["keyfile"]),
        ),
        db=DbSettings(
            host=_get_env("DB_HOST") or str(db["host"]),
            port=_get_int_env("DB_PORT", int(db["port"])),
            name=_get_env("DB_NAME") or str(db["name"]),
            username=_get_env("DB_USERNAME") or str(db["username"]),
            password=_get_env("DB_PASSWORD") or str(db["password"]),
            echo=_get_bool_env("DB_ECHO", default=bool(db["echo"])),
        ),
    )
