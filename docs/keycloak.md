# Keycloak

Die Gebrauchtwagen-API nutzt fuer den Mindestnachweis die Keycloak-Installation
aus dem Beispielprojekt.

## Vorhandene Keycloak-Konfiguration

- Realm: `python`
- Client: `python-client`
- Client-Rolle fuer geschuetzte Schreibzugriffe: `admin`
- Beispiel-Benutzer: `admin`
- Beispiel-Passwort: `p`
- Lokale Realm-URL: `https://localhost:8843/realms/python`
- Lokale Token-URL:
  `https://localhost:8843/realms/python/protocol/openid-connect/token`

Der passende Client-Secret-Wert ist in
`src/gebrauchtwagen/config/application.toml` eingetragen und kann ueber
`GEBRAUCHTWAGEN_KEYCLOAK_CLIENT_SECRET` ueberschrieben werden.

## Keycloak lokal starten

Wenn die Named Volumes `kc_data` und `kc_tls` bereits wie im Beispielprojekt
eingerichtet sind:

```powershell
docker compose -f extras\compose\keycloak\compose.yml up -d
```

Die Einrichtung der Volumes und der TLS-Dateien ist im Beispielprojekt
dokumentiert:

```text
C:\Users\anna\dev\extras\compose\keycloak\ReadMe.md
```

## Geschuetzter Pfad

`POST /gebrauchtwagen` ist mit der Keycloak-Client-Rolle `admin` geschuetzt.
`GET /gebrauchtwagen`, `/health` und `/graphql` bleiben fuer den aktuellen
Mindestnachweis ungeschuetzt.

Token ueber die Gebrauchtwagen-API holen:

```powershell
$body = @{ username = "admin"; password = "p" } | ConvertTo-Json
$response = Invoke-RestMethod `
  -Method Post `
  -Uri https://127.0.0.1:8443/auth/token `
  -ContentType "application/json" `
  -Body $body `
  -SkipCertificateCheck
$token = $response.token
```

Geschuetzten Schreibzugriff ausfuehren:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri https://127.0.0.1:8443/gebrauchtwagen `
  -Headers @{ Authorization = "Bearer $token" } `
  -ContentType "application/json" `
  -Body '{"fin":"WVWZZZ1JZXW000001","marke":"Audi","modell":"A3","baujahr":2021,"kilometerstand":25000,"kraftstoffart":"BENZIN","fahrzeugklasse":"KOMPAKTKLASSE","ausstattung":{},"erstzulassung":"2021-03-15","schadenfrei":true,"beschreibung_url":null}' `
  -SkipCertificateCheck
```

Ohne `Authorization: Bearer ...` antwortet `POST /gebrauchtwagen` mit `401`.
