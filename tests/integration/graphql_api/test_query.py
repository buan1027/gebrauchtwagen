"""Integrationstests fuer GraphQL-Queries."""

from http import HTTPStatus

from fastapi.testclient import TestClient
from pytest import mark

from gebrauchtwagen.main import app


@mark.graphql
@mark.query
def test_graphql_query_reads_persisted_gebrauchtwagen() -> None:
    with TestClient(app) as client:
        create_response = client.post(
            "/gebrauchtwagen",
            json={
                "fin": "WVWZZZ1JZXW000003",
                "marke": "BMW",
                "modell": "i3",
                "baujahr": 2019,
                "kilometerstand": 42000,
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
                  }
                }
                """
            },
        )

    assert create_response.status_code == HTTPStatus.CREATED
    assert graphql_response.status_code == HTTPStatus.OK
    assert graphql_response.json() == {
        "data": {
            "gebrauchtwagen": [
                {
                    "id": 1,
                    "version": 1,
                    "fin": "WVWZZZ1JZXW000003",
                    "marke": "BMW",
                    "modell": "i3",
                    "baujahr": 2019,
                    "kilometerstand": 42000,
                }
            ]
        }
    }
