# Git-Workflow

## Grundidee

Wir arbeiten in diesem Projekt direkt auf `main` und nutzen keine
Feature-Branches. Der wichtigste Befehl ist deshalb immer zuerst:

```powershell
git status -sb
```

Die Ausgabe sagt dir, was als Naechstes sinnvoll ist.

## Status lesen

### Alles synchron

```text
## main...origin/main
```

Dein lokaler Stand und GitHub sind synchron. Es gibt nichts zu pullen und nichts
zu pushen.

### Lokale Commits sind noch nicht auf GitHub

```text
## main...origin/main [ahead 2]
```

Du hast lokale Commits, die noch nicht gepusht sind.

```powershell
git push
```

### GitHub ist weiter als dein lokaler Stand

```text
## main...origin/main [behind 2]
```

Du musst den neuesten Stand holen.

```powershell
git pull --ff-only
uv sync
docker compose -f extras\compose\postgres\compose.yml up -d db
.\.venv\Scripts\python.exe -m pytest
uv run ty check
uv run ruff check src tests
```

### Du hast lokale Commits und GitHub ist auch weiter

```text
## main...origin/main [ahead 2, behind 1]
```

Hole zuerst den Remote-Stand. `--ff-only` verhindert automatische Merge-Commits.

```powershell
git pull --ff-only
```

Wenn das sauber durchlaeuft:

```powershell
uv sync
docker compose -f extras\compose\postgres\compose.yml up -d db
.\.venv\Scripts\python.exe -m pytest
uv run ty check
uv run ruff check src tests
git push
```

Wenn `git pull --ff-only` abbricht, hat sich die Historie verzweigt. Dann nicht
blind mergen, sondern im Team klaeren.

## Aenderungen committen

Vor dem Commit:

```powershell
git status -sb
git diff
```

Dann gezielt die passenden Dateien stagen:

```powershell
git add <datei-oder-verzeichnis>
git diff --cached --stat
git commit -m "feat: kurze Beschreibung (#22)"
```

Wenn mehrere fachliche Aenderungen entstanden sind, lieber mehrere kleine
Commits machen, z. B. Abhaengigkeiten, Feature-Code, Tests und Doku getrennt.

## Vor dem Push

Der kurze Standardcheck:

```powershell
git status -sb
git pull --ff-only
uv sync
docker compose -f extras\compose\postgres\compose.yml up -d db
.\.venv\Scripts\python.exe -m pytest
uv run ty check
uv run ruff check src tests
git push
```

Wenn `uv run ruff check src tests` bekannte Nacharbeiten zeigt, die bewusst von
einem anderen Teammitglied uebernommen werden, dann im Commit-/Ticket-Kontext
notieren und zumindest die geaenderten Dateien gezielt pruefen.

## Faustregeln

- Immer mit `git status -sb` beginnen.
- Bei `[behind ...]` zuerst `git pull --ff-only`.
- Bei `[ahead ...]` und sauberem Stand ist `git push` der richtige naechste
  Schritt.
- Bei `[ahead ..., behind ...]` erst pullen, testen, dann pushen.
- Uncommittete Aenderungen vor einem Pull bewusst committen oder nur ausnahmsweise
  stashen.
- Keine automatischen Merge-Commits auf `main`, solange der einfache
  `--ff-only`-Workflow reicht.
