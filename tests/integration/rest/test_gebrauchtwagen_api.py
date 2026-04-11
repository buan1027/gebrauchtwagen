"""Integrationstests fuer die REST-API."""

from http import HTTPStatus

from fastapi.testclient import TestClient
from pytest import mark

from gebrauchtwagen.main import app


@mark.rest
@mark.post_request
def test_create_gebrauchtwagen_returns_response_dto() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/gebrauchtwagen",
            json={
                "fin": "WVWZZZ1JZXW000001",
                "marke": "Audi",
                "modell": "A3",
                "baujahr": 2021,
                "kilometerstand": 25000,
            },
        )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "version": 1,
        "fin": "WVWZZZ1JZXW000001",
        "marke": "Audi",
        "modell": "A3",
        "baujahr": 2021,
        "kilometerstand": 25000,
    }


@mark.rest
@mark.post_request
def test_create_gebrauchtwagen_rejects_invalid_payload() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/gebrauchtwagen",
            json={
                "fin": "",
                "marke": "  ",
                "modell": "A3",
                "baujahr": 1800,
                "kilometerstand": -10,
            },
        )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    body = response.json()
    assert body["title"] == "Unprocessable Content"
    assert body["status_code"] == HTTPStatus.UNPROCESSABLE_ENTITY
    errors = body["detail"]
    error_fields = {
        ".".join(str(part) for part in error["loc"][1:]) for error in errors
    }

    assert {"fin", "marke", "baujahr", "kilometerstand"}.issubset(error_fields)


@mark.rest
@mark.get_request
def test_unknown_path_returns_problem_details_404() -> None:
    with TestClient(app) as client:
        response = client.get("/unbekannt")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.headers["content-type"].startswith("application/problem+json")
    assert response.json() == {
        "title": "Not Found",
        "status_code": HTTPStatus.NOT_FOUND,
        "detail": "Der Pfad wurde nicht gefunden: /unbekannt",
    }


@mark.rest
@mark.get_request
def test_get_gebrauchtwagen_returns_empty_list_for_empty_database() -> None:
    with TestClient(app) as client:
        response = client.get("/gebrauchtwagen")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


@mark.rest
@mark.get_request
def test_get_gebrauchtwagen_returns_serialized_list() -> None:
    with TestClient(app) as client:
        create_response = client.post(
            "/gebrauchtwagen",
            json={
                "fin": "WVWZZZ1JZXW000001",
                "marke": "Audi",
                "modell": "A3",
                "baujahr": 2021,
                "kilometerstand": 25000,
            },
        )

        list_response = client.get("/gebrauchtwagen")

    assert create_response.status_code == HTTPStatus.CREATED
    assert list_response.status_code == HTTPStatus.OK
    assert list_response.json() == [
        {
            "id": 1,
            "version": 1,
            "fin": "WVWZZZ1JZXW000001",
            "marke": "Audi",
            "modell": "A3",
            "baujahr": 2021,
            "kilometerstand": 25000,
        }
    ]


@mark.rest
@mark.get_request
def test_persisted_gebrauchtwagen_survives_new_client() -> None:
    with TestClient(app) as client:
        create_response = client.post(
            "/gebrauchtwagen",
            json={
                "fin": "WVWZZZ1JZXW000002",
                "marke": "VW",
                "modell": "Golf",
                "baujahr": 2020,
                "kilometerstand": 30000,
            },
        )

    with TestClient(app) as client:
        list_response = client.get("/gebrauchtwagen")

    assert create_response.status_code == HTTPStatus.CREATED
    assert list_response.status_code == HTTPStatus.OK
    assert list_response.json() == [
        {
            "id": 1,
            "version": 1,
            "fin": "WVWZZZ1JZXW000002",
            "marke": "VW",
            "modell": "Golf",
            "baujahr": 2020,
            "kilometerstand": 30000,
        }
    ]


@mark.rest
@mark.health
def test_health_reports_connected_database(monkeypatch) -> None:
    monkeypatch.setattr(
        "gebrauchtwagen.router.health_router.is_database_connected",
        lambda: True,
    )

    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "ok", "database": "connected"}


@mark.rest
@mark.health
def test_health_reports_disconnected_database(monkeypatch) -> None:
    monkeypatch.setattr(
        "gebrauchtwagen.router.health_router.is_database_connected",
        lambda: False,
    )

    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "degraded", "database": "disconnected"}
