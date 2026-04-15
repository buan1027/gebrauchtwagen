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
- NVD API Key: optional ueber Umgebungsvariable `NVD_API_KEY`

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

## Nachweis vom 15.04.2026

Installierte Version vor dem Update:

```text
Dependency-Check Core version 12.2.0
```

Ausgefuehrter Befehl:

```powershell
uv run extras\dependency-check.py
```

Ergebnis:

```text
[INFO] Checking for updates
[WARN] An NVD API Key was not provided
[ERROR] Error updating the NVD Data
Cannot deserialize value of type `java.time.ZonedDateTime` from String
"2026-04-15T15:21:48.700955Z"
[ERROR] Unable to continue dependency-check analysis.
```

Der Ablauf ist damit im Projekt vorhanden und wurde gestartet. Ein vollstaendiger
Bericht konnte mit Dependency-Check `12.2.0` in dieser Umgebung noch nicht
erzeugt werden, weil die Aktualisierung der NVD-Daten vor der Projektanalyse
abbricht. Fuer den naechsten erfolgreichen Lauf sollte ein NVD API Key gesetzt
und, falls der Parse-Fehler weiter besteht, die lokale Dependency-Check-
Installation aktualisiert werden.

Ein zweiter Lauf mit einem temporaer gesetzten NVD API Key aus dem
Beispielprojekt beseitigte die Warnung zum fehlenden API Key, scheiterte aber
weiterhin an demselben NVD-Zeitstempel-Parse-Fehler. Damit ist der fehlende Key
nicht die Ursache des aktuellen Abbruchs.

Anschliessend wurde die lokale Installation unter `C:\Zimmermann` reversibel von
Dependency-Check `12.2.0` auf `12.2.1` aktualisiert. Die vorherige Installation
liegt als Backup unter `C:\Zimmermann\dependency-check-12.2.0`.

Installierte Version nach dem Update:

```text
Dependency-Check Core version 12.2.1
```

Auch mit `12.2.1` scheitert der Lauf weiterhin beim Aktualisieren der NVD-Daten:

```text
Cannot deserialize value of type `java.time.ZonedDateTime` from String
"2026-04-15T16:12:06.798407900Z"
```

Ein weiterer Lauf mit `12.2.1` und temporaer gesetztem NVD API Key scheiterte
ebenfalls an demselben Zeitstempel-Parse-Fehler. Damit sind sowohl der fehlende
API Key als auch die lokale Version `12.2.0` als alleinige Ursache
ausgeschlossen.

## Offene Rueckfrage

Da der Fehler vor der eigentlichen Projektanalyse beim NVD-Datenupdate auftritt,
wurde am 15.04.2026 eine Rueckfrage im ILIAS-Forum der Veranstaltung erstellt.
Die Frage klaert, ob fuer die Veranstaltung ein bestimmter Workaround erwartet
wird, zum Beispiel eine andere Dependency-Check-Version, ein vorbereiteter
`dependency-check-data`-Cache oder eine alternative Konfiguration.
