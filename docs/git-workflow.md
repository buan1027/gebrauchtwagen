# Git-Workflow zum Aktualisieren und Testen

## Warum diese Datei im Repository liegt

Diese Anleitung ist Team-Dokumentation und soll bewusst versioniert werden.
Darum gehoert sie **nicht** in `.gitignore`.

Ein eigener `docs`-Ordner ist sinnvoll, weil hier spaeter weitere kurze
Anleitungen fuer typische Entwicklungsablaeufe gesammelt werden koennen.

## Normaler Workflow

```powershell
git status
git fetch --all --prune
git pull --ff-only
.\.venv\Scripts\python.exe -m pytest
```

### Bedeutung der Befehle

`git status`
Zeigt dir den aktuellen Zustand deines Repos:
- Auf welchem Branch du bist
- Ob du lokale, uncommittete Aenderungen hast
- Ob dein Branch vor oder hinter dem Remote liegt

`git fetch --all --prune`
Laedt neue Informationen vom Remote, ohne deinen aktuellen Branch zu veraendern.
- `fetch`: Holt neue Commits und Branch-Informationen
- `--all`: Holt von allen eingetragenen Remotes
- `--prune`: Entfernt veraltete Remote-Referenzen lokal

`git pull --ff-only`
Uebernimmt die Aenderungen vom Remote in deinen aktuellen Branch.
- `pull`: Kombination aus `fetch` plus Integration
- `--ff-only`: Nur erlauben, wenn ein Fast-Forward moeglich ist
- Vorteil: Kein automatischer Merge-Commit, kein ungewolltes Vermischen von Staenden

`.\.venv\Scripts\python.exe -m pytest`
Startet die Tests mit dem Python-Interpreter aus deiner virtuellen Umgebung.
- `.\`: Datei aus dem aktuellen Verzeichnis verwenden
- `.venv\Scripts\python.exe`: Python aus dem Projekt-Virtualenv
- `-m pytest`: Fuehrt das Python-Modul `pytest` aus

## Wenn lokale Aenderungen vorhanden sind

```powershell
git status
git add .
git commit -m "WIP: lokaler Zwischenstand"
git fetch --all --prune
git pull --ff-only
.\.venv\Scripts\python.exe -m pytest
```

### Bedeutung

`git add .`
Nimmt alle Aenderungen im aktuellen Verzeichnis in die Staging Area auf.

`git commit -m "WIP: lokaler Zwischenstand"`
Speichert deinen aktuellen Stand lokal als Commit.
- `-m`: Uebergibt die Commit-Nachricht direkt
- `WIP`: Bedeutet meist "Work in Progress"

Das ist sinnvoll, wenn du deine Aenderungen sichern willst, bevor du den
neuesten Stand holst.

## Wenn du noch nicht committen willst

```powershell
git status
git stash push -m "temporaer vor pull"
git fetch --all --prune
git pull --ff-only
git stash pop
.\.venv\Scripts\python.exe -m pytest
```

### Bedeutung

`git stash push -m "temporaer vor pull"`
Legt deine uncommitteten Aenderungen voruebergehend beiseite.
- `stash`: Zwischenspeicher fuer lokale Aenderungen
- `push`: Erstellt einen neuen Stash
- `-m`: Gibt dem Stash eine Beschreibung

`git stash pop`
Holt die zwischengespeicherten Aenderungen zurueck und entfernt den Stash danach.

Hinweis: Wenn sich dein lokaler Code und die neuen Remote-Aenderungen an
denselben Stellen ueberschneiden, kann es dabei zu Konflikten kommen.

## Faustregeln

- `git status` immer zuerst
- `git fetch` zum sicheren Pruefen neuer Remote-Aenderungen
- `git pull --ff-only` fuer kontrolliertes Aktualisieren
- `python -m pytest` zum Verifizieren nach dem Update
- `commit`, wenn du deinen Stand bewusst sichern willst
- `stash`, wenn du nur kurz Platz schaffen willst

## Kurzfassung

```powershell
git status
git fetch --all --prune
git pull --ff-only
.\.venv\Scripts\python.exe -m pytest
```
