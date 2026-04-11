# Git-Workflow

## Ziel

Diese Anleitung beschreibt den einfachen Standardablauf fuer dieses Projekt.
Wir arbeiten bewusst direkt auf `main` und nutzen keine Feature-Branches.

## Aktuellen Stand holen

Nutze diesen Ablauf, wenn du den neuesten Stand aus GitHub holen und lokal
pruefen willst:

```powershell
git status
git fetch --prune
git pull --ff-only
uv sync
docker compose -f extras\compose\postgres\compose.yml up -d db
.\.venv\Scripts\python.exe -m pytest
uv run ty check
uv run ruff check src tests
```

### Bedeutung

`git status`
Zeigt dir den aktuellen Zustand deines Repos:
- ob du auf `main` bist
- ob du lokale, uncommittete Aenderungen hast
- ob dein lokaler Stand vor oder hinter dem Remote liegt

`git fetch --prune`
Laedt neue Informationen vom Remote, ohne deinen lokalen Stand zu veraendern.

`git pull --ff-only`
Uebernimmt die Aenderungen vom Remote in deinen lokalen `main`-Stand.
`--ff-only` verhindert automatische Merge-Commits.

`uv sync`
Bringt die lokale `.venv` auf den Stand aus `pyproject.toml` und `uv.lock`.
Das ist wichtig, wenn beim Pull neue Abhaengigkeiten oder Tools dazugekommen
sind.

`docker compose -f extras\compose\postgres\compose.yml up -d db`
Startet die lokale PostgreSQL-Datenbank im Hintergrund. Die API-Tests brauchen
diese Datenbank.

`pytest`, `ty` und `ruff`
Pruefen, ob Tests, Typpruefung und Linting weiterhin erfolgreich sind.

## Eigene Aenderungen veroeffentlichen

Nutze diesen Ablauf, wenn du deine lokalen Aenderungen fertig hast:

```powershell
git status
git add <dateien>
git commit -m "docs: Git-Workflow aktualisieren (#17)"
git status
git pull --ff-only
uv sync
docker compose -f extras\compose\postgres\compose.yml up -d db
.\.venv\Scripts\python.exe -m pytest
uv run ty check
uv run ruff check src tests
git push
```

### Bedeutung

`git add <dateien>`
Nimmt ausgewaehlte Dateien in die Staging Area auf. Die Staging Area ist die
Vorbereitung fuer den naechsten Commit: Du sammelst dort bewusst, was gleich
gespeichert werden soll.

`git commit -m "..."`
Speichert den gestagten Stand lokal als Commit.
- Der erste Teil beschreibt die Art der Aenderung, zum Beispiel `feat`, `fix`,
  `docs`, `chore` oder `refactor`.
- Wenn es ein passendes Issue gibt, haengen wir die Nummer an, zum Beispiel
  `(#17)`.
- Bei kleinen Hygiene-Fixes ohne Issue kann die Nummer weggelassen werden.

`git pull --ff-only`
Prueft vor dem Push noch einmal, ob inzwischen neue Remote-Aenderungen vorhanden
sind. Wenn ja, werden sie nur uebernommen, wenn ein Fast-Forward moeglich ist.

`docker compose -f extras\compose\postgres\compose.yml up -d db`
Stellt sicher, dass die Datenbank fuer die Tests laeuft.

`git push`
Veroeffentlicht deine lokalen Commits auf GitHub.

## Wenn lokale Aenderungen vor dem Pull vorhanden sind

Wenn `git status` lokale Aenderungen zeigt, bevor du pullst, entscheide zuerst:
- committen, wenn du deinen Stand bewusst sichern willst
- oder `git stash` nur als Ausnahme, wenn du wirklich nicht committen willst

Fuer dieses Projekt ist ein bewusster Commit meistens der klarere Weg.

## Faustregeln

- `git status` immer zuerst
- auf `main` bleiben
- vor dem Push noch einmal `git pull --ff-only` ausfuehren
- vor dem Push Tests, `ty` und `ruff` ausfuehren
- `git push` erst nach erfolgreichen Checks
