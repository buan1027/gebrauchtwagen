# OWASP Dependency-Check

## Zweck

OWASP steht fuer Open Worldwide Application Security Project. Der OWASP
Dependency-Check ist ein Werkzeug zur Software-Composition-Analyse: Er gleicht
Projektabhaengigkeiten gegen bekannte Schwachstellen aus CVE-/NVD-Daten ab.

Fuer den Gebrauchtwagen-Server bedeutet das: Die in `pyproject.toml` und
`uv.lock` dokumentierten Drittanbieter-Bibliotheken werden auf bekannte
Schwachstellen geprueft. Der erzeugte HTML-/JSON-Bericht dient als
nachvollziehbarer Sicherheitsnachweis.

## Projektanpassung

Der Ablauf wurde aus dem Beispielprojekt unter `C:\Users\anna\dev` uebernommen
und angepasst:

- Projektname: `gebrauchtwagen`
- Skript: `extras\dependency-check.py`
- Suppression-Datei: `extras\dependency-check-suppression.xml`
- Scan-Ziel: Repository-Root mit `pyproject.toml` und `uv.lock`
- Berichtsziel: `reports\dependency-check\`
- NVD API Key: empfohlen ueber Umgebungsvariable `NVD_API_KEY`; alternativ
  lokal im Skript als `nvd_api_key`

Die Suppression-Datei ist bewusst leer. Es gibt aktuell keine begruendete
False-Positive-Ausnahme fuer dieses Projekt.

## Ausfuehrung

```powershell
uv run extras\dependency-check.py
```

Optional mit NVD API Key:

```powershell
$env:NVD_API_KEY = "<dein-api-key>"
uv run extras\dependency-check.py
```

Alternativ kann der eigene Key analog zum Beispielprojekt lokal direkt in
`extras\dependency-check.py` als Wert von `nvd_api_key` eingetragen werden. Vor
einem Commit muss der Wert wieder entfernt werden. Die Umgebungsvariable hat
Vorrang, falls beide Varianten gesetzt sind.

## Nachweis vom 16.04.2026

Installierte Version:

```text
Dependency-Check Core version 12.2.1
```

Fuer die Ausfuehrung wurde ein eigener NVD API Key lokal ueber die
Umgebungsvariable `NVD_API_KEY` bereitgestellt. Der Key wird nicht im Repository
gespeichert.

Ausgefuehrter Befehl:

```powershell
uv run extras\dependency-check.py
```

Ergebnis:

```text
[INFO] Check for updates complete
[INFO] Analysis Started
[INFO] Analysis Complete (5 seconds)
[INFO] Writing HTML report to:
C:\Users\anna\gebrauchtwagen\reports\dependency-check\dependency-check-report.html
[INFO] Writing JSON report to:
C:\Users\anna\gebrauchtwagen\reports\dependency-check\dependency-check-report.json
```

Der vollstaendige Lauf wurde mit Dependency-Check `12.2.1` und eigenem NVD API
Key erfolgreich ausgefuehrt. Die erzeugten Reports liegen lokal unter
`reports\dependency-check\`. Dieses Verzeichnis ist in `.gitignore`
ausgeschlossen, damit generierte Berichte nicht ins Repository eingecheckt
werden.
