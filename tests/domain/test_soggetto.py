"""Test del layer Domain: entità Soggetto."""
import pytest
from uuid import uuid4

from src.domain.entities.soggetto import Soggetto


def test_soggetto_creazione_valida():
    s = Soggetto(
        codice_fiscale="RSSMRA80A01H501U",
        denominazione="Mario Rossi",
        natura_giuridica="PF",
    )
    assert s.codice_fiscale == "RSSMRA80A01H501U"
    assert s.natura_giuridica == "PF"
    assert s.id is not None


def test_soggetto_persona_giuridica():
    s = Soggetto(
        codice_fiscale="12345678901",
        denominazione="Acme S.p.A.",
        natura_giuridica="PG",
        partita_iva="12345678901",
    )
    assert s.natura_giuridica == "PG"
    assert s.partita_iva == "12345678901"


def test_soggetto_codice_fiscale_vuoto():
    with pytest.raises(ValueError, match="codice fiscale"):
        Soggetto(
            codice_fiscale="",
            denominazione="Mario Rossi",
            natura_giuridica="PF",
        )


def test_soggetto_natura_giuridica_non_valida():
    with pytest.raises(ValueError, match="natura giuridica"):
        Soggetto(
            codice_fiscale="RSSMRA80A01H501U",
            denominazione="Mario Rossi",
            natura_giuridica="XX",
        )
