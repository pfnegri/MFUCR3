"""Domain service: calcolo e valutazione del rischio credito di un soggetto."""
from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from src.domain.entities.rischio_credito import RischioCredito
from src.domain.repositories.posizione_creditizia_repository import (
    PosizioneCreditiziaRepository,
)


class RischioCreditoService:
    """Servizio di dominio per l'elaborazione del rischio di credito."""

    def __init__(self, posizione_repo: PosizioneCreditiziaRepository) -> None:
        self._posizione_repo = posizione_repo

    def calcola_rischio(self, soggetto_id: UUID) -> RischioCredito:
        """Aggrega tutte le posizioni del soggetto in un RischioCredito."""
        posizioni = self._posizione_repo.trova_per_soggetto(soggetto_id)
        rischio = RischioCredito(soggetto_id=soggetto_id)
        for posizione in posizioni:
            rischio.aggiungi_posizione(posizione)
        return rischio

    def soggetto_in_sofferenza(self, soggetto_id: UUID) -> bool:
        """Ritorna True se il soggetto ha almeno una posizione in sofferenza."""
        rischio = self.calcola_rischio(soggetto_id)
        return rischio.esposizione_in_sofferenza > Decimal("0")
