"""Test del layer Domain: entità PosizioneCreditizia."""
import pytest
from datetime import date
from decimal import Decimal
from uuid import uuid4

from src.domain.entities.posizione_creditizia import PosizioneCreditizia


def _posizione(**kwargs) -> PosizioneCreditizia:
    defaults = dict(
        soggetto_id=uuid4(),
        intermediario_abi="03069",
        importo_accordato=Decimal("100000"),
        importo_utilizzato=Decimal("50000"),
        categoria_censimento="A_REVOCA",
        data_segnalazione=date(2024, 1, 31),
    )
    defaults.update(kwargs)
    return PosizioneCreditizia(**defaults)


def test_posizione_valida():
    p = _posizione()
    assert p.margine_disponibile == Decimal("50000")


def test_posizione_importo_utilizzato_supera_accordato():
    with pytest.raises(ValueError, match="importo utilizzato"):
        _posizione(importo_accordato=Decimal("50000"), importo_utilizzato=Decimal("60000"))


def test_posizione_importo_accordato_negativo():
    with pytest.raises(ValueError, match="importo accordato"):
        _posizione(importo_accordato=Decimal("-1"))


def test_posizione_categoria_non_valida():
    with pytest.raises(ValueError, match="Categoria"):
        _posizione(categoria_censimento="SCONOSCIUTA")


def test_posizione_margine_zero_quando_tutto_utilizzato():
    p = _posizione(importo_accordato=Decimal("1000"), importo_utilizzato=Decimal("1000"))
    assert p.margine_disponibile == Decimal("0")
