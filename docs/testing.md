# Tests

## Ziel

Diese Anleitung beschreibt, wie du die Tests lokal ausfuehrst und was die
ueblichen Varianten sind.

## Standard-Testlauf

```powershell
.\.venv\Scripts\python.exe -m pytest
```

### Warum dieser Befehl robust ist

- Er verwendet direkt den Python-Interpreter aus der virtuellen Umgebung
- `-m pytest` startet das installierte Modul mit genau diesem Interpreter
- Dadurch nutzt du nicht versehentlich ein global installiertes `pytest`

## Alternative mit `uv`

```powershell
uv run pytest
```

Das ist kuerzer und normalerweise ebenfalls passend, solange `uv` lokal sauber
funktioniert.

## Typpruefung mit ty

```powershell
uv run ty check
```

### Bedeutung

- Fuehrt die statische Typpruefung mit `ty` aus
- Meldet Typfehler frueh, bevor sie zur Laufzeit auffallen

## Nur einen Bereich testen

```powershell
.\.venv\Scripts\python.exe -m pytest tests\integration\rest
.\.venv\Scripts\python.exe -m pytest tests\integration\graphql_api
```

## Mehr Details im Output

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

### Bedeutung

`-v`
- Steht fuer `verbose`
- Zeigt mehr Details zu einzelnen Testfaellen

## Nach einem Pull testen

Der uebliche Ablauf ist:

```powershell
git pull --ff-only
docker compose -f extras\compose\postgres\compose.yml up -d db
.\.venv\Scripts\python.exe -m pytest
```

## Was ein gutes Ergebnis ist

Ein erfolgreicher Lauf sieht typischerweise so aus:

- Alle Tests sind `passed`
- Es gibt keine Fehler oder Abbrueche
- Warnungen koennen vorkommen, sollten aber bewusst eingeordnet werden

## Wenn Tests fehlschlagen

Pruefe zuerst:

- Wurde `uv sync` nach neuen Abhaengigkeiten ausgefuehrt?
- Laeuft die lokale Datenbank, falls ein Test sie benoetigt?
- Nutzt du wirklich die Projekt-Umgebung und nicht globales Python?
