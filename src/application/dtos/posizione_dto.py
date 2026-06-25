"""DTO per le Posizioni Creditizie e il Rischio Credito."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import List
from uuid import UUID


@dataclass(frozen=True)
class PosizioneCrediziziaDTO:
    id: UUID
    soggetto_id: UUID
    intermediario_abi: str
    importo_accordato: Decimal
    importo_utilizzato: Decimal
    categoria_censimento: str
    data_segnalazione: date
    margine_disponibile: Decimal


@dataclass(frozen=True)
class CreaPosizioneCommand:
    soggetto_id: UUID
    intermediario_abi: str
    importo_accordato: Decimal
    importo_utilizzato: Decimal
    categoria_censimento: str
    data_segnalazione: date


@dataclass(frozen=True)
class RischioCreditoDTO:
    soggetto_id: UUID
    esposizione_totale: Decimal
    accordato_totale: Decimal
    esposizione_in_sofferenza: Decimal
    posizioni: List[PosizioneCrediziziaDTO] = field(default_factory=list)
