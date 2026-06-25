"""Schemi Pydantic per i Soggetti (request/response)."""
from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CreaSoggettoRequest(BaseModel):
    codice_fiscale: str = Field(..., description="Codice fiscale del soggetto")
    denominazione: str = Field(..., description="Nome o ragione sociale")
    natura_giuridica: str = Field(
        ..., description="'PF' per persona fisica, 'PG' per persona giuridica"
    )
    partita_iva: Optional[str] = Field(None, description="Partita IVA (opzionale)")


class SoggettoResponse(BaseModel):
    id: UUID
    codice_fiscale: str
    denominazione: str
    natura_giuridica: str
    partita_iva: Optional[str] = None
