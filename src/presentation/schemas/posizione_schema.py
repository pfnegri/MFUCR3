"""Schemi Pydantic per le Posizioni Creditizie e il Rischio Credito."""
from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class CreaPosizioneRequest(BaseModel):
    soggetto_id: UUID
    intermediario_abi: str = Field(..., description="Codice ABI dell'intermediario")
    importo_accordato: Decimal = Field(..., ge=0, description="Fido accordato in euro")
    importo_utilizzato: Decimal = Field(
        ..., ge=0, description="Importo utilizzato in euro"
    )
    categoria_censimento: str = Field(
        ...,
        description="Categoria: AUTOLIQUIDANTI, A_SCADENZA, A_REVOCA, SOFFERENZE, INCAGLI",
    )
    data_segnalazione: date = Field(..., description="Data della segnalazione (YYYY-MM-DD)")


class PosizioneResponse(BaseModel):
    id: UUID
    soggetto_id: UUID
    intermediario_abi: str
    importo_accordato: Decimal
    importo_utilizzato: Decimal
    categoria_censimento: str
    data_segnalazione: date
    margine_disponibile: Decimal


class RischioCreditoResponse(BaseModel):
    soggetto_id: UUID
    esposizione_totale: Decimal
    accordato_totale: Decimal
    esposizione_in_sofferenza: Decimal
    posizioni: List[PosizioneResponse] = []
