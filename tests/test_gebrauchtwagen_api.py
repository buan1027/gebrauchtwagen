from fastapi.testclient import TestClient
import pytest

from gebrauchtwagen.main import app


@pytest.fixture(autouse=True)
def reset_store(monkeypatch):
    monkeypatch.setattr("gebrauchtwagen.main._gebrauchtwagen_store", [])


def test_create_gebrauchtwagen_returns_response_dto(monkeypatch) -> None:
    monkeypatch.setattr("gebrauchtwagen.main.check_database_connection", lambda: None)
    monkeypatch.setattr("gebrauchtwagen.main.create_tables", lambda: None)

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

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "version": 1,
        "fin": "WVWZZZ1JZXW000001",
        "marke": "Audi",
        "modell": "A3",
        "baujahr": 2021,
        "kilometerstand": 25000,
    }


def test_create_gebrauchtwagen_rejects_invalid_payload(monkeypatch) -> None:
    monkeypatch.setattr("gebrauchtwagen.main.check_database_connection", lambda: None)
    monkeypatch.setattr("gebrauchtwagen.main.create_tables", lambda: None)
    monkeypatch.setattr("gebrauchtwagen.main.engine.dispose", lambda: None)

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

    assert response.status_code == 422
    body = response.json()
    assert body["title"] == "Unprocessable Content"
    assert body["status_code"] == 422
    errors = body["detail"]
    error_fields = {".".join(str(part) for part in error["loc"][1:]) for error in errors}

    assert {"fin", "marke", "baujahr", "kilometerstand"}.issubset(error_fields)


def test_unknown_path_returns_problem_details_404(monkeypatch) -> None:
    monkeypatch.setattr("gebrauchtwagen.main.check_database_connection", lambda: None)
    monkeypatch.setattr("gebrauchtwagen.main.create_tables", lambda: None)
    monkeypatch.setattr("gebrauchtwagen.main.engine.dispose", lambda: None)

    with TestClient(app) as client:
        response = client.get("/unbekannt")

    assert response.status_code == 404
    assert response.headers["content-type"].startswith("application/problem+json")
    assert response.json() == {
        "title": "Not Found",
        "status_code": 404,
        "detail": "Der Pfad wurde nicht gefunden: /unbekannt",
    }


def test_get_gebrauchtwagen_returns_empty_list_for_empty_database(monkeypatch) -> None:
    monkeypatch.setattr("gebrauchtwagen.main.check_database_connection", lambda: None)
    monkeypatch.setattr("gebrauchtwagen.main.create_tables", lambda: None)

    with TestClient(app) as client:
        response = client.get("/gebrauchtwagen")

    assert response.status_code == 200
    assert response.json() == []


def test_get_gebrauchtwagen_returns_serialized_list(monkeypatch) -> None:
    monkeypatch.setattr("gebrauchtwagen.main.check_database_connection", lambda: None)
    monkeypatch.setattr("gebrauchtwagen.main.create_tables", lambda: None)

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

    assert create_response.status_code == 201
    assert list_response.status_code == 200
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


def test_health_reports_connected_database(monkeypatch) -> None:
    monkeypatch.setattr("gebrauchtwagen.main.check_database_connection", lambda: None)
    monkeypatch.setattr("gebrauchtwagen.main.create_tables", lambda: None)
    monkeypatch.setattr("gebrauchtwagen.main.is_database_connected", lambda: True)

    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "connected"}


def test_health_reports_disconnected_database(monkeypatch) -> None:
    monkeypatch.setattr("gebrauchtwagen.main.check_database_connection", lambda: None)
    monkeypatch.setattr("gebrauchtwagen.main.create_tables", lambda: None)
    monkeypatch.setattr("gebrauchtwagen.main.is_database_connected", lambda: False)

    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "degraded", "database": "disconnected"}
