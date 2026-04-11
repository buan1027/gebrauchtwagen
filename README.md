# gebrauchtwagen

Ein FastAPI-Projekt fuer eine Gebrauchtwagen-Anwendung.

## Voraussetzungen

- VS Code mit Python-Erweiterung
- `uv`
- Python 3.14

## Start

```powershell
uv sync
docker compose -f extras\compose\postgres\compose.yml up -d db
uv run gebrauchtwagen
```

## Browser

Im Browser kannst du danach `https://127.0.0.1:8443` und
`https://127.0.0.1:8443/health` aufrufen.

## Tests

```powershell
docker compose -f extras\compose\postgres\compose.yml up -d db
uv run pytest
```

Weitere kurze Team-Dokumentation liegt unter `docs/`, zum Beispiel zu Git,
lokalem Setup, Tests und Troubleshooting.

## Lokales TLS

Die Zertifikatsdateien werden bewusst **nicht** ins Repository eingecheckt.
Jede Person im Team erzeugt die Dateien lokal unter:

`src/gebrauchtwagen/config/resources/tls/`

Erwartete Dateinamen:
- `certificate.pem`
- `key.pem`

Solange diese Dateien fehlen, kann der HTTPS-Start noch nicht funktionieren.
Die Pfade dafuer stehen in `src/gebrauchtwagen/config/application.toml`.

## Lokale Datenbank

Die Anwendung erwartet lokal eine PostgreSQL-Datenbank mit den Werten aus
`src/gebrauchtwagen/config/application.toml`.

Starten kannst du sie mit:

```powershell
docker compose -f extras\compose\postgres\compose.yml up -d db
```
