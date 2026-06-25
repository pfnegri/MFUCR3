"""Test del layer Application: SoggettoService."""
import pytest
from uuid import uuid4

from src.application.dtos.soggetto_dto import CreaSoggettoCommand
from src.application.use_cases.soggetto_service import SoggettoService
from src.infrastructure.repositories.in_memory_soggetto_repository import (
    InMemorySoggettoRepository,
)


@pytest.fixture
def service():
    return SoggettoService(InMemorySoggettoRepository())


def test_crea_soggetto(service):
    cmd = CreaSoggettoCommand(
        codice_fiscale="RSSMRA80A01H501U",
        denominazione="Mario Rossi",
        natura_giuridica="PF",
    )
    dto = service.crea_soggetto(cmd)
    assert dto.codice_fiscale == "RSSMRA80A01H501U"
    assert dto.id is not None


def test_crea_soggetto_duplicato(service):
    cmd = CreaSoggettoCommand(
        codice_fiscale="RSSMRA80A01H501U",
        denominazione="Mario Rossi",
        natura_giuridica="PF",
    )
    service.crea_soggetto(cmd)
    with pytest.raises(ValueError, match="già presente"):
        service.crea_soggetto(cmd)


def test_ottieni_soggetto_non_esistente(service):
    assert service.ottieni_soggetto(uuid4()) is None


def test_lista_soggetti_vuota(service):
    assert service.lista_soggetti() == []


def test_lista_soggetti(service):
    for i in range(3):
        service.crea_soggetto(
            CreaSoggettoCommand(
                codice_fiscale=f"CF{i:015d}",
                denominazione=f"Soggetto {i}",
                natura_giuridica="PF",
            )
        )
    assert len(service.lista_soggetti()) == 3


def test_elimina_soggetto(service):
    dto = service.crea_soggetto(
        CreaSoggettoCommand(
            codice_fiscale="RSSMRA80A01H501U",
            denominazione="Mario Rossi",
            natura_giuridica="PF",
        )
    )
    service.elimina_soggetto(dto.id)
    assert service.ottieni_soggetto(dto.id) is None


def test_elimina_soggetto_non_esistente(service):
    with pytest.raises(ValueError, match="non trovato"):
        service.elimina_soggetto(uuid4())
