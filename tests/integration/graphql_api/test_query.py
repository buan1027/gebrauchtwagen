"""Integrationstests fuer GraphQL-Queries."""

from http import HTTPStatus

from fastapi.testclient import TestClient
from pytest import mark

from gebrauchtwagen.main import app

AUTH_HEADERS = {"Authorization": "Bearer integration-test-token"}


@mark.graphql
@mark.query
def test_graphql_query_reads_persisted_gebrauchtwagen() -> None:
    with TestClient(app) as client:
        create_response = client.post(
            "/gebrauchtwagen",
            headers=AUTH_HEADERS,
            json={
                "fin": "WVWZZZ1JZXW000003",
                "marke": "BMW",
                "modell": "i3",
                "baujahr": 2019,
                "kilometerstand": 42000,
                "kraftstoffart": "ELEKTRO",
                "fahrzeugklasse": "KOMPAKTKLASSE",
                "ausstattung": {"waermepumpe": True},
                "erstzulassung": "2019-05-20",
                "schadenfrei": True,
                "beschreibung_url": None,
            },
        )

        graphql_response = client.post(
            "/graphql",
            json={
                "query": """
                query {
                  gebrauchtwagen {
                    id
                    version
                    fin
                    marke
                    modell
                    baujahr
                    kilometerstand
                                        kraftstoffart
                                        fahrzeugklasse
                                        ausstattung
                                        erstzulassung
                                        schadenfrei
                                        beschreibungUrl
                                        erzeugt
                                        aktualisiert
                  }
                }
                """
            },
        )

    assert create_response.status_code == HTTPStatus.CREATED
    assert graphql_response.status_code == HTTPStatus.OK
    payload = graphql_response.json()
    items = payload["data"]["gebrauchtwagen"]
    assert len(items) == 1
    item = items[0]
    assert isinstance(item.pop("erzeugt"), str)
    assert isinstance(item.pop("aktualisiert"), str)
    assert item == {
        "id": 1,
        "version": 1,
        "fin": "WVWZZZ1JZXW000003",
        "marke": "BMW",
        "modell": "i3",
        "baujahr": 2019,
        "kilometerstand": 42000,
        "kraftstoffart": "ELEKTRO",
        "fahrzeugklasse": "KOMPAKTKLASSE",
        "ausstattung": {"waermepumpe": True},
        "erstzulassung": "2019-05-20",
        "schadenfrei": True,
        "beschreibungUrl": None,
    }
