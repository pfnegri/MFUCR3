"""Entità PosizioneCredizizia: esposizione creditizia di un soggetto verso un intermediario."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4


@dataclass
class PosizioneCredizizia:
    """Rappresenta l'esposizione creditizia di un soggetto verso un intermediario."""

    soggetto_id: UUID
    intermediario_abi: str
    importo_accordato: Decimal
    importo_utilizzato: Decimal
    categoria_censimento: str  # es. "AUTOLIQUIDANTI", "A_SCADENZA", "A_REVOCA", "SOFFERENZE"
    data_segnalazione: date
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if self.importo_accordato < Decimal("0"):
            raise ValueError("L'importo accordato non può essere negativo.")
        if self.importo_utilizzato < Decimal("0"):
            raise ValueError("L'importo utilizzato non può essere negativo.")
        if self.importo_utilizzato > self.importo_accordato:
            raise ValueError(
                "L'importo utilizzato non può superare l'importo accordato."
            )
        categorie_valide = {
            "AUTOLIQUIDANTI",
            "A_SCADENZA",
            "A_REVOCA",
            "SOFFERENZE",
            "INCAGLI",
        }
        if self.categoria_censimento not in categorie_valide:
            raise ValueError(
                f"Categoria di censimento non valida. Valori ammessi: {categorie_valide}"
            )

    @property
    def margine_disponibile(self) -> Decimal:
        """Margine non ancora utilizzato."""
        return self.importo_accordato - self.importo_utilizzato
