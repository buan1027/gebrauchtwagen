# Troubleshooting

## `git pull --ff-only` bricht ab

Das bedeutet meistens:
- Du hast lokale Commits, die nicht auf dem Remote sind
- Oder dein lokaler `main`-Stand und `origin/main` sind auseinander gelaufen

Typische erste Checks:

```powershell
git status
git log --oneline --decorate --graph --all -20
```

Wenn du uncommittete Aenderungen hast, entscheide zuerst:
- committen
- stashen
- oder bewusst verwerfen

## `pytest` oder Python laufen nicht wie erwartet

Pruefe, ob die virtuelle Umgebung vorhanden ist:

```powershell
Get-ChildItem .venv\Scripts
```

Wenn noetig, richte die Umgebung neu ein:

```powershell
uv sync
```

Danach erneut testen:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## `uv run pytest` macht lokal Probleme

Dann ist dieser Fallback oft die bessere Wahl:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Damit umgehst du Probleme beim Start ueber `uv` und verwendest direkt den
Interpreter der lokalen Projektumgebung.

## Die Anwendung startet nicht wegen TLS

Pruefe, ob diese Dateien existieren:

- `src/gebrauchtwagen/config/resources/tls/certificate.pem`
- `src/gebrauchtwagen/config/resources/tls/key.pem`

Wenn sie fehlen, kann der HTTPS-Start nicht funktionieren.

## Die Anwendung erreicht die Datenbank nicht

Pruefe zuerst, ob der Container laeuft:

```powershell
docker compose -f extras\compose\postgres\compose.yml ps
```

Bei Bedarf neu starten:

```powershell
docker compose -f extras\compose\postgres\compose.yml up -d db
```

Die erwarteten lokalen Verbindungsdaten stehen in
`src/gebrauchtwagen/config/application.toml`.
