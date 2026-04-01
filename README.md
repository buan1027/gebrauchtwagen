# gebrauchtwagen

Ein FastAPI-Projekt für eine Gebrauchtwagen-Anwendung.

## Voraussetzungen

- VS Code mit Python-Erweiterung
- `uv`
- Python 3.14

## Start

```powershell
uv sync
uv run gebrauchtwagen
```

## Browser

Im Browser kannst man danach `https://127.0.0.1:8443` und
`https://127.0.0.1:8443/health` aufrufen.

## Tests

```powershell
uv run pytest
```

## Lokales TLS

Die Zertifikatsdateien werden bewusst **nicht** ins Repository eingecheckt.
Jede Person im Team erzeugt die Dateien lokal unter:

`src/gebrauchtwagen/config/resources/tls/`

Erwartete Dateinamen:
- `certificate.pem`
- `key.pem`

Solange diese Dateien fehlen, kann der HTTPS-Start noch nicht funktionieren.
Die Pfade dafür stehen in `src/gebrauchtwagen/config/application.toml`.
