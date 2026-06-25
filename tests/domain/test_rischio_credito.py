"""Test del layer Domain: entità RischioCredito e domain service."""
from datetime import date
from decimal import Decimal
from uuid import uuid4

from src.domain.entities.posizione_creditizia import PosizioneCredizizia
from src.domain.entities.rischio_credito import RischioCredito
from src.domain.services.rischio_credito_service import RischioCreditoService
from src.infrastructure.repositories.in_memory_posizione_creditizia_repository import (
    InMemoryPosizioneCrediziziaRepository,
)


def _make_posizione(soggetto_id, categoria, accordato, utilizzato):
    return PosizioneCredizizia(
        soggetto_id=soggetto_id,
        intermediario_abi="03069",
        importo_accordato=Decimal(str(accordato)),
        importo_utilizzato=Decimal(str(utilizzato)),
        categoria_censimento=categoria,
        data_segnalazione=date(2024, 1, 31),
    )


def test_rischio_credito_aggregazione():
    soggetto_id = uuid4()
    rischio = RischioCredito(soggetto_id=soggetto_id)
    p1 = _make_posizione(soggetto_id, "A_REVOCA", 100000, 40000)
    p2 = _make_posizione(soggetto_id, "SOFFERENZE", 20000, 20000)
    rischio.aggiungi_posizione(p1)
    rischio.aggiungi_posizione(p2)

    assert rischio.esposizione_totale == Decimal("60000")
    assert rischio.accordato_totale == Decimal("120000")
    assert rischio.esposizione_in_sofferenza == Decimal("20000")


def test_rischio_credito_soggetto_diverso():
    import pytest
    soggetto_id = uuid4()
    altro_id = uuid4()
    rischio = RischioCredito(soggetto_id=soggetto_id)
    p = _make_posizione(altro_id, "A_REVOCA", 10000, 5000)
    with pytest.raises(ValueError):
        rischio.aggiungi_posizione(p)


def test_domain_service_soggetto_in_sofferenza():
    repo = InMemoryPosizioneCrediziziaRepository()
    soggetto_id = uuid4()
    p = _make_posizione(soggetto_id, "SOFFERENZE", 5000, 5000)
    repo.salva(p)

    service = RischioCreditoService(repo)
    assert service.soggetto_in_sofferenza(soggetto_id) is True


def test_domain_service_soggetto_non_in_sofferenza():
    repo = InMemoryPosizioneCrediziziaRepository()
    soggetto_id = uuid4()
    p = _make_posizione(soggetto_id, "A_REVOCA", 10000, 3000)
    repo.salva(p)

    service = RischioCreditoService(repo)
    assert service.soggetto_in_sofferenza(soggetto_id) is False
