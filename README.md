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

## Docker-Image fuer den Appserver

Das Dockerfile basiert auf der Vorlage aus dem Beispielprojekt und ist auf die
Gebrauchtwagen-API angepasst.

Image bauen:

```powershell
docker build --tag gebrauchtwagen:0.1.0 .
```

Container gegen die lokal laufende PostgreSQL-Datenbank starten:

```powershell
docker run --rm --publish 8000:8000 --env GEBRAUCHTWAGEN_DB_HOST=host.docker.internal gebrauchtwagen:0.1.0
```

Im Container lauscht die App auf `0.0.0.0:8000`. Der Datenbank-Host kann ueber
`GEBRAUCHTWAGEN_DB_HOST` gesetzt werden. Fuer ein spaeteres Compose-Setup ist
als Standard `db` vorgesehen.

## Docker Compose fuer App und Datenbank

Das Compose-Setup folgt der Struktur aus dem Beispielprojekt: `backend` bindet
die Infrastruktur ein, `gebrauchtwagen` startet zusaetzlich den Appserver.

Voraussetzung ist, dass das Image `gebrauchtwagen:0.1.0` lokal gebaut wurde.

```powershell
cd extras\compose\gebrauchtwagen
docker compose up
```

Beenden:

```powershell
docker compose down
```

Die App ist im Compose-Setup unter `http://127.0.0.1:8000` erreichbar.
