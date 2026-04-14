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
lokalem Setup, Tests, Keycloak und Troubleshooting.

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

Die Docker-Builds basieren auf Varianten aus dem Beispielprojekt.

- `Dockerfile.trixie`: Standardvariante fuer Team-Entwicklung und CI (empfohlen)
- `Dockerfile.alpine`: zusaetzliche, schlanke Variante
- `docker-bake.hcl`: zentrale Build-Definition fuer beide Targets

Die Variante `hardened` wird aktuell bewusst nicht uebernommen, weil der
zusatzliche Hardening-Aufwand (z. B. restriktivere Laufzeitparameter und
projektweite Security-Ausnahmen) fuer den aktuellen Projektstand noch keinen
Mehrwert gegenueber `trixie` liefert.

Empfohlenes Standard-Image bauen:

```powershell
docker buildx bake trixie
```

Zusaetzliche Variante bauen:

```powershell
docker buildx bake alpine
```

Alternativ (ohne Bake) bleibt der bisherige Build nutzbar:

```powershell
docker build --tag gebrauchtwagen:0.1.0 .
```

Container gegen die lokal laufende PostgreSQL-Datenbank und Keycloak aus dem
Beispielprojekt starten:

```powershell
docker run --rm `
  --publish 8000:8000 `
  --env GEBRAUCHTWAGEN_DB_HOST=host.docker.internal `
  --env GEBRAUCHTWAGEN_KEYCLOAK_HOST=host.docker.internal `
  gebrauchtwagen:trixie
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

## Keycloak / OIDC

Fuer den Mindestnachweis wird die Keycloak-Konfiguration aus dem Beispielprojekt
verwendet:

- Realm: `python`
- Client: `python-client`
- benoetigte Client-Rolle fuer `POST /gebrauchtwagen`: `admin`

Keycloak kann mit der uebernommenen Compose-Vorlage gestartet werden, wenn die
Named Volumes `kc_data` und `kc_tls` gemaess Beispielprojekt eingerichtet sind:

```powershell
docker compose -f extras\compose\keycloak\compose.yml up -d
```

Ein Token fuer den Beispielbenutzer `admin` kann ueber die API abgeholt werden:

```powershell
$body = @{ username = "admin"; password = "p" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri https://127.0.0.1:8443/auth/token -ContentType "application/json" -Body $body -SkipCertificateCheck
```

Weitere Details stehen in `docs/keycloak.md`.
