# Bruno Requests

## Ziel

Diese kleine Bruno-Sammlung hilft bei manuellen lokalen API-Tests.

## Ort

Collection und Requests liegen unter:

- `extras/bruno/gebrauchtwagen-api/`

Enthalten sind:

- `REST/GET-gebrauchtwagen.bru`
- `REST/POST-gebrauchtwagen.bru`
- `GraphQL/GraphQL-gebrauchtwagen.bru`
- `environments/local.bru`

## Nutzung

1. In Bruno den Ordner `extras/bruno/gebrauchtwagen-api` als Collection oeffnen.
2. Das Environment `local` aktivieren.
3. Lokal die Datenbank und API starten.
4. GET, POST und GraphQL-Query ausfuehren.

```powershell
docker compose -f extras\compose\postgres\compose.yml up -d db
uv run gebrauchtwagen
```

## VS-Code-Erweiterung

1. Das Bruno-Icon in der linken Seitenleiste oeffnen.
2. Ueber das Collection-Menue `Open Collection` auswaehlen.
3. Den Ordner `extras/bruno/gebrauchtwagen-api` oeffnen.
4. Das Environment `local` auswaehlen.
5. Bei Bedarf die SSL-Verifikation fuer lokale Tests deaktivieren.

Hinweis:
- Lokal wird ein selbstsigniertes TLS-Zertifikat verwendet. Falls noetig, in Bruno die Zertifikatspruefung fuer lokale Tests deaktivieren.
