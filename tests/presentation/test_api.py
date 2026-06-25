"""Test del layer Presentation: API endpoints FastAPI."""
import pytest
from datetime import date
from decimal import Decimal
from fastapi.testclient import TestClient

from main import app
from src.presentation.api.dependencies import (
    get_soggetto_service,
    get_centrale_rischi_service,
)
from src.application.use_cases.soggetto_service import SoggettoService
from src.application.use_cases.centrale_rischi_service import CentraleRischiService
from src.infrastructure.repositories.in_memory_soggetto_repository import (
    InMemorySoggettoRepository,
)
from src.infrastructure.repositories.in_memory_posizione_creditizia_repository import (
    InMemoryPosizioneCreditiziaRepository,
)


@pytest.fixture
def client():
    """Client con repository freschi per ogni test."""
    soggetto_repo = InMemorySoggettoRepository()
    posizione_repo = InMemoryPosizioneCreditiziaRepository()

    app.dependency_overrides[get_soggetto_service] = lambda: SoggettoService(soggetto_repo)
    app.dependency_overrides[get_centrale_rischi_service] = lambda: CentraleRischiService(
        soggetto_repo, posizione_repo
    )

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


def test_crea_soggetto(client):
    resp = client.post(
        "/soggetti/",
        json={
            "codice_fiscale": "RSSMRA80A01H501U",
            "denominazione": "Mario Rossi",
            "natura_giuridica": "PF",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["codice_fiscale"] == "RSSMRA80A01H501U"
    assert "id" in data


def test_crea_soggetto_duplicato(client):
    payload = {
        "codice_fiscale": "RSSMRA80A01H501U",
        "denominazione": "Mario Rossi",
        "natura_giuridica": "PF",
    }
    client.post("/soggetti/", json=payload)
    resp = client.post("/soggetti/", json=payload)
    assert resp.status_code == 400


def test_lista_soggetti_vuota(client):
    resp = client.get("/soggetti/")
    assert resp.status_code == 200
    assert resp.json() == []


def test_ottieni_soggetto_non_trovato(client):
    import uuid
    resp = client.get(f"/soggetti/{uuid.uuid4()}")
    assert resp.status_code == 404


def test_elimina_soggetto(client):
    resp = client.post(
        "/soggetti/",
        json={
            "codice_fiscale": "RSSMRA80A01H501U",
            "denominazione": "Mario Rossi",
            "natura_giuridica": "PF",
        },
    )
    soggetto_id = resp.json()["id"]
    del_resp = client.delete(f"/soggetti/{soggetto_id}")
    assert del_resp.status_code == 204


def test_registra_posizione_e_rischio(client):
    # Crea soggetto
    resp = client.post(
        "/soggetti/",
        json={
            "codice_fiscale": "RSSMRA80A01H501U",
            "denominazione": "Mario Rossi",
            "natura_giuridica": "PF",
        },
    )
    soggetto_id = resp.json()["id"]

    # Registra posizione
    pos_resp = client.post(
        "/centrale-rischi/posizioni",
        json={
            "soggetto_id": soggetto_id,
            "intermediario_abi": "03069",
            "importo_accordato": "50000",
            "importo_utilizzato": "20000",
            "categoria_censimento": "A_REVOCA",
            "data_segnalazione": "2024-01-31",
        },
    )
    assert pos_resp.status_code == 201
    assert pos_resp.json()["margine_disponibile"] == "30000"

    # Ottieni rischio
    rischio_resp = client.get(f"/centrale-rischi/soggetti/{soggetto_id}/rischio")
    assert rischio_resp.status_code == 200
    rischio = rischio_resp.json()
    assert rischio["esposizione_totale"] == "20000"
    assert len(rischio["posizioni"]) == 1


def test_rischio_soggetto_non_trovato(client):
    import uuid
    resp = client.get(f"/centrale-rischi/soggetti/{uuid.uuid4()}/rischio")
    assert resp.status_code == 404
