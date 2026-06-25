"""Entità RischioCredito: aggregato del rischio complessivo di un soggetto."""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import List
from uuid import UUID, uuid4

from .posizione_creditizia import PosizioneCreditizia


@dataclass
class RischioCredito:
    """Aggregato del rischio di credito complessivo di un soggetto."""

    soggetto_id: UUID
    posizioni: List[PosizioneCreditizia] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)

    @property
    def esposizione_totale(self) -> Decimal:
        """Somma degli importi utilizzati su tutte le posizioni."""
        return sum((p.importo_utilizzato for p in self.posizioni), Decimal("0"))

    @property
    def accordato_totale(self) -> Decimal:
        """Somma degli importi accordati su tutte le posizioni."""
        return sum((p.importo_accordato for p in self.posizioni), Decimal("0"))

    @property
    def esposizione_in_sofferenza(self) -> Decimal:
        """Importo totale classificato come sofferenza."""
        return sum(
            (
                p.importo_utilizzato
                for p in self.posizioni
                if p.categoria_censimento == "SOFFERENZE"
            ),
            Decimal("0"),
        )

    def aggiungi_posizione(self, posizione: PosizioneCreditizia) -> None:
        if posizione.soggetto_id != self.soggetto_id:
            raise ValueError(
                "La posizione non appartiene al soggetto di questo rischio credito."
            )
        self.posizioni.append(posizione)
