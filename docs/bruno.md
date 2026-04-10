# Bruno Requests

## Ziel

Diese kleine Bruno-Sammlung hilft bei manuellen lokalen API-Tests.

## Ort

Collection und Requests liegen unter:

- `bruno/gebrauchtwagen-api/`

Enthalten sind:

- `GET-gebrauchtwagen.bru`
- `POST-gebrauchtwagen.bru`
- `environments/local.bru`

## Nutzung

1. In Bruno den Ordner `bruno/gebrauchtwagen-api` als Collection oeffnen.
2. Das Environment `local` aktivieren.
3. Lokal die API starten (`uv run gebrauchtwagen`).
4. GET und POST Requests ausfuehren.

Hinweis:
- Lokal wird ein selbstsigniertes TLS-Zertifikat verwendet. Falls noetig, in Bruno die Zertifikatspruefung fuer lokale Tests deaktivieren.