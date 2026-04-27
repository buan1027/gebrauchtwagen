# Lokales Setup

## Ziel

Diese Anleitung beschreibt die ueblichen Schritte, um das Projekt lokal zu
starten.

## Voraussetzungen

- Python 3.14
- `uv`
- Docker beziehungsweise Docker Desktop
- VS Code mit Python-Erweiterung ist hilfreich, aber nicht zwingend

## Projekt vorbereiten

```powershell
uv sync
```

### Bedeutung

`uv sync`
- Liest die Abhaengigkeiten aus `pyproject.toml` und `uv.lock`
- Erstellt oder aktualisiert die virtuelle Umgebung
- Installiert die benoetigten Pakete fuer das Projekt

## Lokale Datenbank starten

```powershell
docker compose -f extras\compose\postgres\compose.yml up -d db
```

### Bedeutung

`docker compose -f extras\compose\postgres\compose.yml up`
- Erstellt und startet Container aus der Compose-Datei unter
  `extras\compose\postgres\compose.yml`

`-d`
- Startet den Container im Hintergrund

`db`
- Startet nur den Datenbank-Service

Die lokale Datenbank laeuft mit diesen Werten:
- Host: `127.0.0.1`
- Port: `5432`
- Datenbank: `gebrauchtwagen`
- Benutzer: `gebrauchtwagen`
- Passwort: `gebrauchtwagen`

## Datenbankschema und Beispieldaten laden

Die SQL- und CSV-Dateien fuer das relationale Zielmodell liegen unter:

`extras\compose\postgres\init\gebrauchtwagen\`

Schema erzeugen:

```powershell
docker exec gebrauchtwagen-db psql -U gebrauchtwagen -d gebrauchtwagen -v ON_ERROR_STOP=1 -f /init/gebrauchtwagen/sql/create-schema.sql
```

Beispieldaten reproduzierbar laden:

```powershell
docker exec gebrauchtwagen-db psql -U gebrauchtwagen -d gebrauchtwagen -v ON_ERROR_STOP=1 -f /init/gebrauchtwagen/sql/load-csv.sql
```

## TLS-Dateien vorbereiten

Die Anwendung erwartet lokal zwei Dateien unter:

`src/gebrauchtwagen/config/resources/tls/`

Erwartete Dateinamen:
- `certificate.pem`
- `key.pem`

Diese Dateien sind bewusst nicht im Repository eingecheckt.

## Anwendung starten

```powershell
uv run gebrauchtwagen
```

## Anwendung aufrufen

Danach kannst du im Browser aufrufen:

- `https://127.0.0.1:8443`
- `https://127.0.0.1:8443/health`

## Kurzfassung

```powershell
uv sync
docker compose -f extras\compose\postgres\compose.yml up -d db
uv run gebrauchtwagen
```
