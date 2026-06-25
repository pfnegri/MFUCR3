"""DTO (Data Transfer Object) per i Soggetti."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class SoggettoDTO:
    id: UUID
    codice_fiscale: str
    denominazione: str
    natura_giuridica: str
    partita_iva: Optional[str] = None


@dataclass(frozen=True)
class CreaSoggettoCommand:
    codice_fiscale: str
    denominazione: str
    natura_giuridica: str
    partita_iva: Optional[str] = None
