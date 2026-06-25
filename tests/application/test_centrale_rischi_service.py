"""Test del layer Application: CentraleRischiService."""
import pytest
from datetime import date
from decimal import Decimal
from uuid import uuid4

from src.application.dtos.soggetto_dto import CreaSoggettoCommand
from src.application.dtos.posizione_dto import CreaPosizioneCommand
from src.application.use_cases.soggetto_service import SoggettoService
from src.application.use_cases.centrale_rischi_service import CentraleRischiService
from src.infrastructure.repositories.in_memory_soggetto_repository import (
    InMemorySoggettoRepository,
)
from src.infrastructure.repositories.in_memory_posizione_creditizia_repository import (
    InMemoryPosizioneCreditiziaRepository,
)


@pytest.fixture
def repos():
    soggetto_repo = InMemorySoggettoRepository()
    posizione_repo = InMemoryPosizioneCreditiziaRepository()
    return soggetto_repo, posizione_repo


@pytest.fixture
def services(repos):
    soggetto_repo, posizione_repo = repos
    soggetto_service = SoggettoService(soggetto_repo)
    cr_service = CentraleRischiService(soggetto_repo, posizione_repo)
    return soggetto_service, cr_service


@pytest.fixture
def soggetto_id(services):
    soggetto_service, _ = services
    dto = soggetto_service.crea_soggetto(
        CreaSoggettoCommand(
            codice_fiscale="RSSMRA80A01H501U",
            denominazione="Mario Rossi",
            natura_giuridica="PF",
        )
    )
    return dto.id


def test_registra_posizione(services, soggetto_id):
    _, cr_service = services
    cmd = CreaPosizioneCommand(
        soggetto_id=soggetto_id,
        intermediario_abi="03069",
        importo_accordato=Decimal("50000"),
        importo_utilizzato=Decimal("20000"),
        categoria_censimento="A_REVOCA",
        data_segnalazione=date(2024, 1, 31),
    )
    dto = cr_service.registra_posizione(cmd)
    assert dto.soggetto_id == soggetto_id
    assert dto.margine_disponibile == Decimal("30000")


def test_registra_posizione_soggetto_non_trovato(services):
    _, cr_service = services
    with pytest.raises(ValueError, match="non trovato"):
        cr_service.registra_posizione(
            CreaPosizioneCommand(
                soggetto_id=uuid4(),
                intermediario_abi="03069",
                importo_accordato=Decimal("10000"),
                importo_utilizzato=Decimal("5000"),
                categoria_censimento="A_SCADENZA",
                data_segnalazione=date(2024, 1, 31),
            )
        )


def test_ottieni_rischio_soggetto(services, soggetto_id):
    _, cr_service = services
    for categoria, accordato, utilizzato in [
        ("A_REVOCA", 100000, 40000),
        ("SOFFERENZE", 20000, 20000),
    ]:
        cr_service.registra_posizione(
            CreaPosizioneCommand(
                soggetto_id=soggetto_id,
                intermediario_abi="03069",
                importo_accordato=Decimal(str(accordato)),
                importo_utilizzato=Decimal(str(utilizzato)),
                categoria_censimento=categoria,
                data_segnalazione=date(2024, 1, 31),
            )
        )
    rischio = cr_service.ottieni_rischio_soggetto(soggetto_id)
    assert rischio is not None
    assert rischio.esposizione_totale == Decimal("60000")
    assert rischio.esposizione_in_sofferenza == Decimal("20000")
    assert len(rischio.posizioni) == 2


def test_ottieni_rischio_soggetto_non_trovato(services):
    _, cr_service = services
    assert cr_service.ottieni_rischio_soggetto(uuid4()) is None
