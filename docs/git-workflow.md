# Git-Workflow zum Aktualisieren und Testen

## Warum diese Datei im Repository liegt

Diese Anleitung ist Team-Dokumentation und soll bewusst versioniert werden.
Darum gehoert sie **nicht** in `.gitignore`.

Ein eigener `docs`-Ordner ist sinnvoll, weil hier spaeter weitere kurze
Anleitungen fuer typische Entwicklungsablaeufe gesammelt werden koennen.

## Normaler Workflow

Dieses Projekt arbeitet bewusst direkt auf `main`. Die folgenden Schritte gehen
also davon aus, dass `git status` `main` als aktuellen Stand zeigt.

```powershell
git status
git fetch --prune
git pull --ff-only
uv sync
docker compose -f extras\compose\postgres\compose.yml up -d db
.\.venv\Scripts\python.exe -m pytest
```

### Bedeutung der Befehle

`git status`
Zeigt dir den aktuellen Zustand deines Repos:
- Ob du auf `main` bist
- Ob du lokale, uncommittete Aenderungen hast
- Ob dein lokaler Stand vor oder hinter dem Remote liegt

`git fetch --prune`
Laedt neue Informationen vom Remote, ohne deinen lokalen Stand zu veraendern.
- `fetch`: Holt neue Commits und Remote-Informationen
- `--prune`: Entfernt veraltete Remote-Referenzen lokal

`git pull --ff-only`
Uebernimmt die Aenderungen vom Remote in deinen lokalen `main`-Stand.
- `pull`: Kombination aus `fetch` plus Integration
- `--ff-only`: Nur erlauben, wenn ein Fast-Forward moeglich ist
- Vorteil: Kein automatischer Merge-Commit, kein ungewolltes Vermischen von Staenden

`uv sync`
Bringt die lokale `.venv` auf den Stand aus `pyproject.toml` und `uv.lock`.
Das ist besonders wichtig, wenn beim Pull neue Abhaengigkeiten oder Tooling wie
`ty` dazugekommen sind.

`docker compose -f extras\compose\postgres\compose.yml up -d db`
Startet die lokale PostgreSQL-Datenbank im Hintergrund. Die API-Tests brauchen
diese Datenbank, weil sie Tabellen anlegen und Testdaten schreiben.

`.\.venv\Scripts\python.exe -m pytest`
Startet die Tests mit dem Python-Interpreter aus deiner virtuellen Umgebung.
- `.\`: Datei aus dem aktuellen Verzeichnis verwenden
- `.venv\Scripts\python.exe`: Python aus dem Projekt-Virtualenv
- `-m pytest`: Fuehrt das Python-Modul `pytest` aus

## Wenn lokale Aenderungen vorhanden sind

```powershell
git status
git add .
git commit -m "docs: Git-Workflow vereinfachen (#17)"
git fetch --prune
git pull --ff-only
uv sync
docker compose -f extras\compose\postgres\compose.yml up -d db
.\.venv\Scripts\python.exe -m pytest
```

### Bedeutung

`git add .`
Nimmt alle Aenderungen im aktuellen Verzeichnis in die Staging Area auf.
Die Staging Area ist die Vorbereitung fuer den naechsten Commit: Du sammelst
dort bewusst, was gleich gespeichert werden soll.

`git commit -m "docs: Git-Workflow vereinfachen (#17)"`
Speichert deinen aktuellen Stand lokal als Commit.
- `-m`: Uebergibt die Commit-Nachricht direkt
- `docs`: Beschreibt die Art der Aenderung
- `#17`: Referenziert das passende Issue

Das ist sinnvoll, wenn du deine Aenderungen sichern willst, bevor du den
neuesten Stand holst. Wenn du wirklich nur kurz Platz schaffen willst, gibt es
auch `git stash`; fuer dieses Projekt sollte das aber eher die Ausnahme bleiben
und nicht der normale Aktualisierungsweg sein.

## Faustregeln

- `git status` immer zuerst
- Fuer dieses Projekt auf `main` bleiben
- `git fetch` zum sicheren Pruefen neuer Remote-Aenderungen
- `git pull --ff-only` fuer kontrolliertes Aktualisieren
- `uv sync` ausfuehren, wenn sich Abhaengigkeiten oder Tools geaendert haben
- `docker compose -f extras\compose\postgres\compose.yml up -d db` vor den
  API-Tests starten
- `python -m pytest` zum Verifizieren nach dem Update
- `commit`, wenn du deinen Stand bewusst sichern willst
- `stash` nur als Ausnahme, wenn du wirklich nicht committen willst
