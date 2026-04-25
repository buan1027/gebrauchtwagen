# ER-Diagramm

## Ziel

Das ER-Diagramm beschreibt das relationale Zielmodell fuer die
Gebrauchtwagen-Domaene im PostgreSQL-Schema `gebrauchtwagen`.

Die PlantUML-Quelle liegt unter:

[er-diagramm.plantuml](diagramme/src/er-diagramm.plantuml)

## Modell

```mermaid
erDiagram
    GEBRAUCHTWAGEN ||--|| STANDORT : hat
    GEBRAUCHTWAGEN ||--o{ SCHADEN : dokumentiert
    GEBRAUCHTWAGEN ||--|| HAUPTUNTERSUCHUNG : hat

    GEBRAUCHTWAGEN {
        integer id PK
        integer version
        text fin UK
        text marke
        text modell
        integer baujahr
        date erstzulassung
        integer kilometerstand
        Kraftstoffart kraftstoffart
        Fahrzeugklasse fahrzeugklasse
        jsonb ausstattung
        boolean schadenfrei
        text beschreibung_url
        text anbieter_username
        text kontakt_email
        timestamp erzeugt
        timestamp aktualisiert
    }

    STANDORT {
        integer id PK
        text plz
        text ort
        integer gebrauchtwagen_id FK_UK
    }

    SCHADEN {
        integer id PK
        text bezeichnung
        text beschreibung
        date feststellungsdatum
        integer gebrauchtwagen_id FK
    }

    HAUPTUNTERSUCHUNG {
        integer id PK
        date pruefdatum
        date gueltig_bis
        text prueforganisation
        HuStatus status
        integer gebrauchtwagen_id FK_UK
    }
```

## Kardinalitaeten

| Beziehung | Kardinalitaet | Umsetzung |
|---|---:|---|
| Gebrauchtwagen - Standort | 1:1 | `standort.gebrauchtwagen_id` ist Foreign Key und unique |
| Gebrauchtwagen - Schaden | 1:n | `schaden.gebrauchtwagen_id` ist Foreign Key ohne Unique Constraint |
| Gebrauchtwagen - Hauptuntersuchung | 1:1 | `hauptuntersuchung.gebrauchtwagen_id` ist Foreign Key und unique |

## Wichtige Constraints

- `gebrauchtwagen.fin` ist eindeutig.
- Alle Tabellen liegen im Schema `gebrauchtwagen`.
- Die Enum-Typen `kraftstoffart`, `fahrzeugklasse` und `hu_status` liegen ebenfalls im Schema `gebrauchtwagen`.
- `version` ist im ORM als `version_id_col` hinterlegt und bildet die Grundlage fuer optimistische Synchronisation.
- `anbieter_username` und `kontakt_email` erweitern das urspruengliche Zielmodell, damit objektbezogene Zugriffskontrolle und fachliche Kontaktzuordnung spaeter darstellbar sind.

## DDL-Bezug

Die SQL-Umsetzung ist hier dokumentiert:

- `extras/compose/postgres/init/gebrauchtwagen/sql/create-schema.sql`
- `extras/compose/postgres/init/gebrauchtwagen/sql/load-csv.sql`
