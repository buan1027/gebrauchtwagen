"""Integrationstests fuer die REST-API."""

from http import HTTPStatus

from fastapi.testclient import TestClient
from pytest import mark

from gebrauchtwagen.main import app

AUTH_HEADERS = {"Authorization": "Bearer integration-test-token"}
AUTH_HEADERS_WITHOUT_ROLE = {
    "Authorization": "Bearer integration-test-token-without-role",
}


def create_payload(fin: str = "WVWZZZ1JZXW000001") -> dict[str, object | None]:
    """Erzeuge einen gueltigen Payload fuer POST-Tests."""
    return {
        "fin": fin,
        "marke": "Audi",
        "modell": "A3",
        "baujahr": 2021,
        "kilometerstand": 25000,
        "kraftstoffart": "BENZIN",
        "fahrzeugklasse": "KOMPAKTKLASSE",
        "ausstattung": {},
        "erstzulassung": "2021-03-15",
        "schadenfrei": True,
        "beschreibung_url": None,
    }


@mark.rest
@mark.post_request
def test_create_gebrauchtwagen_returns_response_dto() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/gebrauchtwagen",
            headers=AUTH_HEADERS,
            json={
                "fin": "WVWZZZ1JZXW000001",
                "marke": "Audi",
                "modell": "A3",
                "baujahr": 2021,
                "kilometerstand": 25000,
                "kraftstoffart": "BENZIN",
                "fahrzeugklasse": "KOMPAKTKLASSE",
                "ausstattung": {"navi": True, "sitzheizung": True},
                "erstzulassung": "2021-03-15",
                "schadenfrei": True,
                "beschreibung_url": None,
            },
        )

    assert response.status_code == HTTPStatus.CREATED
    body = response.json()
    assert isinstance(body.pop("erzeugt"), str)
    assert isinstance(body.pop("aktualisiert"), str)
    assert body == {
        "id": 1,
        "version": 1,
        "fin": "WVWZZZ1JZXW000001",
        "marke": "Audi",
        "modell": "A3",
        "baujahr": 2021,
        "kilometerstand": 25000,
        "kraftstoffart": "BENZIN",
        "fahrzeugklasse": "KOMPAKTKLASSE",
        "ausstattung": {"navi": True, "sitzheizung": True},
        "erstzulassung": "2021-03-15",
        "schadenfrei": True,
        "beschreibung_url": None,
    }


@mark.rest
@mark.post_request
def test_create_gebrauchtwagen_rejects_invalid_payload() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/gebrauchtwagen",
            headers=AUTH_HEADERS,
            json={
                "fin": "",
                "marke": "  ",
                "modell": "A3",
                "baujahr": 1800,
                "kilometerstand": -10,
                "kraftstoffart": "WASSER",
                "fahrzeugklasse": "FAMILIE",
                "ausstattung": [],
                "erstzulassung": "2021-03-15",
                "schadenfrei": True,
                "beschreibung_url": None,
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

    assert {
        "fin",
        "marke",
        "baujahr",
        "kilometerstand",
        "kraftstoffart",
        "fahrzeugklasse",
        "ausstattung",
    }.issubset(error_fields)


@mark.rest
@mark.post_request
def test_create_gebrauchtwagen_rejects_duplicate_fin() -> None:
    payload = create_payload()

    with TestClient(app) as client:
        first_response = client.post(
            "/gebrauchtwagen",
            headers=AUTH_HEADERS,
            json=payload,
        )
        duplicate_response = client.post(
            "/gebrauchtwagen",
            headers=AUTH_HEADERS,
            json=payload,
        )

    assert first_response.status_code == HTTPStatus.CREATED
    assert duplicate_response.status_code == HTTPStatus.CONFLICT
    assert "FIN WVWZZZ1JZXW000001 existiert bereits" in duplicate_response.text


@mark.rest
@mark.post_request
def test_create_gebrauchtwagen_requires_bearer_token() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/gebrauchtwagen",
            json=create_payload(),
        )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@mark.rest
@mark.post_request
def test_create_gebrauchtwagen_rejects_invalid_bearer_token() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/gebrauchtwagen",
            headers={"Authorization": "Bearer invalid-token"},
            json=create_payload(),
        )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@mark.rest
@mark.post_request
def test_create_gebrauchtwagen_requires_admin_role() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/gebrauchtwagen",
            headers=AUTH_HEADERS_WITHOUT_ROLE,
            json=create_payload(),
        )

    assert response.status_code == HTTPStatus.FORBIDDEN


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
            headers=AUTH_HEADERS,
            json={
                "fin": "WVWZZZ1JZXW000001",
                "marke": "Audi",
                "modell": "A3",
                "baujahr": 2021,
                "kilometerstand": 25000,
                "kraftstoffart": "BENZIN",
                "fahrzeugklasse": "KOMPAKTKLASSE",
                "ausstattung": {},
                "erstzulassung": "2021-03-15",
                "schadenfrei": True,
                "beschreibung_url": None,
            },
        )

        list_response = client.get("/gebrauchtwagen")

    assert create_response.status_code == HTTPStatus.CREATED
    assert list_response.status_code == HTTPStatus.OK
    items = list_response.json()
    assert len(items) == 1
    item = items[0]
    assert isinstance(item.pop("erzeugt"), str)
    assert isinstance(item.pop("aktualisiert"), str)
    assert item == {
        "id": 1,
        "version": 1,
        "fin": "WVWZZZ1JZXW000001",
        "marke": "Audi",
        "modell": "A3",
        "baujahr": 2021,
        "kilometerstand": 25000,
        "kraftstoffart": "BENZIN",
        "fahrzeugklasse": "KOMPAKTKLASSE",
        "ausstattung": {},
        "erstzulassung": "2021-03-15",
        "schadenfrei": True,
        "beschreibung_url": None,
    }


@mark.rest
@mark.get_request
def test_persisted_gebrauchtwagen_survives_new_client() -> None:
    with TestClient(app) as client:
        create_response = client.post(
            "/gebrauchtwagen",
            headers=AUTH_HEADERS,
            json={
                "fin": "WVWZZZ1JZXW000002",
                "marke": "VW",
                "modell": "Golf",
                "baujahr": 2020,
                "kilometerstand": 30000,
                "kraftstoffart": "DIESEL",
                "fahrzeugklasse": "KOMPAKTKLASSE",
                "ausstattung": {
                    "assistenz": {
                        "acc": True,
                        "spurhalteassistent": False,
                    },
                    "multimedia": ["carplay", "bluetooth"],
                },
                "erstzulassung": "2020-06-01",
                "schadenfrei": False,
                "beschreibung_url": None,
            },
        )

    with TestClient(app) as client:
        list_response = client.get("/gebrauchtwagen")

    assert create_response.status_code == HTTPStatus.CREATED
    assert list_response.status_code == HTTPStatus.OK
    items = list_response.json()
    assert len(items) == 1
    item = items[0]
    assert isinstance(item.pop("erzeugt"), str)
    assert isinstance(item.pop("aktualisiert"), str)
    assert item == {
        "id": 1,
        "version": 1,
        "fin": "WVWZZZ1JZXW000002",
        "marke": "VW",
        "modell": "Golf",
        "baujahr": 2020,
        "kilometerstand": 30000,
        "kraftstoffart": "DIESEL",
        "fahrzeugklasse": "KOMPAKTKLASSE",
        "ausstattung": {
            "assistenz": {
                "acc": True,
                "spurhalteassistent": False,
            },
            "multimedia": ["carplay", "bluetooth"],
        },
        "erstzulassung": "2020-06-01",
        "schadenfrei": False,
        "beschreibung_url": None,
    }


@mark.rest
@mark.get_request
def test_get_gebrauchtwagen_by_id_returns_gebrauchtwagen() -> None:
    with TestClient(app) as client:
        create_response = client.post(
            "/gebrauchtwagen",
            headers=AUTH_HEADERS,
            json={
                "fin": "WVWZZZ1JZXW000003",
                "marke": "BMW",
                "modell": "3er",
                "baujahr": 2019,
                "kilometerstand": 45000,
                "kraftstoffart": "BENZIN",
                "fahrzeugklasse": "MITTELKLASSE",
                "ausstattung": {},
                "erstzulassung": "2019-09-10",
                "schadenfrei": True,
                "beschreibung_url": None,
            },
        )

        get_response = client.get("/gebrauchtwagen/1")

    assert create_response.status_code == HTTPStatus.CREATED
    assert get_response.status_code == HTTPStatus.OK
    item = get_response.json()
    assert isinstance(item.pop("erzeugt"), str)
    assert isinstance(item.pop("aktualisiert"), str)
    assert item == {
        "id": 1,
        "version": 1,
        "fin": "WVWZZZ1JZXW000003",
        "marke": "BMW",
        "modell": "3er",
        "baujahr": 2019,
        "kilometerstand": 45000,
        "kraftstoffart": "BENZIN",
        "fahrzeugklasse": "MITTELKLASSE",
        "ausstattung": {},
        "erstzulassung": "2019-09-10",
        "schadenfrei": True,
        "beschreibung_url": None,
    }


@mark.rest
@mark.get_request
def test_get_gebrauchtwagen_by_id_returns_404_for_unknown_id() -> None:
    with TestClient(app) as client:
        response = client.get("/gebrauchtwagen/999")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.headers["content-type"].startswith("application/problem+json")
    body = response.json()
    assert body["title"] == "Not Found"
    assert body["status_code"] == HTTPStatus.NOT_FOUND
    assert "Gebrauchtwagen mit ID 999 nicht gefunden" in body["detail"]


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
