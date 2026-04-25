# ER-Diagramm

Das ER-Diagramm beschreibt das relationale Zielmodell fuer die
Gebrauchtwagen-Domaene im PostgreSQL-Schema `gebrauchtwagen`.

![ER-Diagramm](diagramme/out/ER Diagramm.svg)

## Zweck

Das Diagramm zeigt die Tabellen, Enum-Typen und Beziehungen, die fuer die
Persistenz des Gebrauchtwagen-Aggregats verwendet werden. Es dokumentiert damit
den Zielzustand, gegen den ORM-Entities, DDL, CSV-Testdaten und
Integrationstests abgeglichen werden.

Die PlantUML-Quelle liegt unter
[er-diagramm.plantuml](diagramme/src/er-diagramm.plantuml).

## Relationales Modell

| Tabelle | Aufgabe | Primaere fachliche Merkmale |
|---|---|---|
| `gebrauchtwagen.gebrauchtwagen` | Wurzel des Aggregats | FIN, Marke, Modell, Baujahr, Erstzulassung, Kilometerstand, Kraftstoffart, Fahrzeugklasse, Ausstattung, Schadenfreiheit |
| `gebrauchtwagen.standort` | aktueller Standort eines Fahrzeugs | PLZ und Ort, eindeutig einem Gebrauchtwagen zugeordnet |
| `gebrauchtwagen.schaden` | dokumentierte Schaeden eines Fahrzeugs | Bezeichnung, Beschreibung und Feststellungsdatum |
| `gebrauchtwagen.hauptuntersuchung` | aktuelle Hauptuntersuchung eines Fahrzeugs | Pruefdatum, Gueltigkeit, Organisation und Status |

## Enum-Typen

| Enum | Werte |
|---|---|
| `gebrauchtwagen.kraftstoffart` | `BENZIN`, `DIESEL`, `ELEKTRO`, `HYBRID`, `ERDGAS`, `WASSERSTOFF` |
| `gebrauchtwagen.fahrzeugklasse` | `KLEINWAGEN`, `KOMPAKTKLASSE`, `MITTELKLASSE`, `OBERKLASSE`, `SUV`, `KOMBI`, `CABRIO`, `TRANSPORTER` |
| `gebrauchtwagen.hu_status` | `BESTANDEN`, `NICHT_BESTANDEN`, `AUSSTEHEND` |

## Kardinalitaeten

| Beziehung | Kardinalitaet | Umsetzung |
|---|---:|---|
| Gebrauchtwagen - Standort | 1:1 | `standort.gebrauchtwagen_id` ist Foreign Key und unique |
| Gebrauchtwagen - Schaden | 1:n | `schaden.gebrauchtwagen_id` ist Foreign Key ohne Unique Constraint |
| Gebrauchtwagen - Hauptuntersuchung | 1:1 | `hauptuntersuchung.gebrauchtwagen_id` ist Foreign Key und unique |

## Zentrale Constraints

- `gebrauchtwagen.fin` ist eindeutig und bildet die fachliche Fahrzeugkennung.
- Alle Tabellen und Enum-Typen liegen im Schema `gebrauchtwagen`.
- `version` ist im ORM als `version_id_col` hinterlegt und bildet die
  Grundlage fuer optimistische Synchronisation.
- `standort.gebrauchtwagen_id` und `hauptuntersuchung.gebrauchtwagen_id`
  erzwingen jeweils genau eine aktuelle Zuordnung pro Fahrzeug.
- `schaden.gebrauchtwagen_id` erlaubt mehrere dokumentierte Schaeden pro
  Fahrzeug.

## Fachliche Ergaenzungen

Das urspruengliche Zielmodell wurde um `anbieter_username` und `kontakt_email`
erweitert. Damit bleiben spaetere fachliche Anforderungen an objektbezogene
Zugriffskontrolle und Kontaktzuordnung im relationalen Modell darstellbar,
ohne eine eigene Benutzer- oder Anbieter-Tabelle vorwegzunehmen.

## Umsetzung

Die SQL-Umsetzung ist ueber die PostgreSQL-Initialisierung nachvollziehbar:

- `extras/compose/postgres/init/gebrauchtwagen/sql/create-schema.sql`
- `extras/compose/postgres/init/gebrauchtwagen/sql/load-csv.sql`

Die dazugehoerigen CSV-Dateien liefern reproduzierbare Beispieldaten fuer alle
Tabellen. `load-csv.sql` leert die Tabellen vor dem Laden mit
`TRUNCATE ... RESTART IDENTITY CASCADE`, damit ein erneuter Ladebefehl denselben
Datenbestand wiederherstellt.
