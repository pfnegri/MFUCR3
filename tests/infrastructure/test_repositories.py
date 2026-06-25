"""Test del layer Infrastructure: repository in-memory."""
from datetime import date
from decimal import Decimal
from uuid import uuid4

from src.domain.entities.soggetto import Soggetto
from src.domain.entities.posizione_creditizia import PosizioneCredizizia
from src.infrastructure.repositories.in_memory_soggetto_repository import (
    InMemorySoggettoRepository,
)
from src.infrastructure.repositories.in_memory_posizione_creditizia_repository import (
    InMemoryPosizioneCrediziziaRepository,
)


def test_soggetto_repo_salva_e_trova_per_id():
    repo = InMemorySoggettoRepository()
    s = Soggetto(
        codice_fiscale="RSSMRA80A01H501U",
        denominazione="Mario Rossi",
        natura_giuridica="PF",
    )
    repo.salva(s)
    assert repo.trova_per_id(s.id) == s


def test_soggetto_repo_trova_per_codice_fiscale():
    repo = InMemorySoggettoRepository()
    s = Soggetto(
        codice_fiscale="RSSMRA80A01H501U",
        denominazione="Mario Rossi",
        natura_giuridica="PF",
    )
    repo.salva(s)
    assert repo.trova_per_codice_fiscale("RSSMRA80A01H501U") == s
    assert repo.trova_per_codice_fiscale("NONEXIST") is None


def test_soggetto_repo_elimina():
    repo = InMemorySoggettoRepository()
    s = Soggetto(
        codice_fiscale="RSSMRA80A01H501U",
        denominazione="Mario Rossi",
        natura_giuridica="PF",
    )
    repo.salva(s)
    repo.elimina(s.id)
    assert repo.trova_per_id(s.id) is None


def test_posizione_repo_trova_per_soggetto():
    repo = InMemoryPosizioneCrediziziaRepository()
    soggetto_id = uuid4()
    altro_id = uuid4()
    for _ in range(2):
        repo.salva(
            PosizioneCredizizia(
                soggetto_id=soggetto_id,
                intermediario_abi="03069",
                importo_accordato=Decimal("10000"),
                importo_utilizzato=Decimal("5000"),
                categoria_censimento="A_REVOCA",
                data_segnalazione=date(2024, 1, 31),
            )
        )
    repo.salva(
        PosizioneCredizizia(
            soggetto_id=altro_id,
            intermediario_abi="03069",
            importo_accordato=Decimal("10000"),
            importo_utilizzato=Decimal("5000"),
            categoria_censimento="A_REVOCA",
            data_segnalazione=date(2024, 1, 31),
        )
    )
    assert len(repo.trova_per_soggetto(soggetto_id)) == 2
    assert len(repo.trova_per_soggetto(altro_id)) == 1
