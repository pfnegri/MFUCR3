"""Entità Soggetto: rappresenta un soggetto censito nella Centrale Rischi."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Soggetto:
    """Soggetto censito nella Centrale Rischi (persona fisica o giuridica)."""

    codice_fiscale: str
    denominazione: str
    natura_giuridica: str  # es. "PF" (persona fisica) o "PG" (persona giuridica)
    id: UUID = field(default_factory=uuid4)
    partita_iva: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.codice_fiscale:
            raise ValueError("Il codice fiscale non può essere vuoto.")
        if not self.denominazione:
            raise ValueError("La denominazione non può essere vuota.")
        if self.natura_giuridica not in ("PF", "PG"):
            raise ValueError(
                "La natura giuridica deve essere 'PF' (persona fisica) o 'PG' (persona giuridica)."
            )
