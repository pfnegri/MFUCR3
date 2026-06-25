"""Use case: gestione delle Posizioni Creditizie e consultazione del Rischio Credito."""
from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from src.domain.entities.posizione_creditizia import PosizioneCredizizia
from src.domain.repositories.posizione_creditizia_repository import (
    PosizioneCrediziziaRepository,
)
from src.domain.repositories.soggetto_repository import SoggettoRepository
from src.domain.services.rischio_credito_service import RischioCreditoService
from src.application.dtos.posizione_dto import (
    CreaPosizioneCommand,
    PosizioneCrediziziaDTO,
    RischioCreditoDTO,
)


def _to_dto(posizione: PosizioneCredizizia) -> PosizioneCrediziziaDTO:
    return PosizioneCrediziziaDTO(
        id=posizione.id,
        soggetto_id=posizione.soggetto_id,
        intermediario_abi=posizione.intermediario_abi,
        importo_accordato=posizione.importo_accordato,
        importo_utilizzato=posizione.importo_utilizzato,
        categoria_censimento=posizione.categoria_censimento,
        data_segnalazione=posizione.data_segnalazione,
        margine_disponibile=posizione.margine_disponibile,
    )


class CentraleRischiService:
    """Orchestrazione dei casi d'uso della Centrale Rischi."""

    def __init__(
        self,
        soggetto_repo: SoggettoRepository,
        posizione_repo: PosizioneCrediziziaRepository,
    ) -> None:
        self._soggetto_repo = soggetto_repo
        self._posizione_repo = posizione_repo
        self._rischio_service = RischioCreditoService(posizione_repo)

    def registra_posizione(
        self, command: CreaPosizioneCommand
    ) -> PosizioneCrediziziaDTO:
        """Registra una nuova posizione creditizia per il soggetto."""
        if self._soggetto_repo.trova_per_id(command.soggetto_id) is None:
            raise ValueError(
                f"Soggetto con id '{command.soggetto_id}' non trovato."
            )
        posizione = PosizioneCredizizia(
            soggetto_id=command.soggetto_id,
            intermediario_abi=command.intermediario_abi,
            importo_accordato=command.importo_accordato,
            importo_utilizzato=command.importo_utilizzato,
            categoria_censimento=command.categoria_censimento,
            data_segnalazione=command.data_segnalazione,
        )
        self._posizione_repo.salva(posizione)
        return _to_dto(posizione)

    def ottieni_posizioni_soggetto(
        self, soggetto_id: UUID
    ) -> List[PosizioneCrediziziaDTO]:
        """Ritorna tutte le posizioni del soggetto."""
        return [
            _to_dto(p)
            for p in self._posizione_repo.trova_per_soggetto(soggetto_id)
        ]

    def ottieni_rischio_soggetto(self, soggetto_id: UUID) -> Optional[RischioCreditoDTO]:
        """Calcola e ritorna il rischio complessivo del soggetto."""
        if self._soggetto_repo.trova_per_id(soggetto_id) is None:
            return None
        rischio = self._rischio_service.calcola_rischio(soggetto_id)
        posizioni_dto = [_to_dto(p) for p in rischio.posizioni]
        return RischioCreditoDTO(
            soggetto_id=rischio.soggetto_id,
            esposizione_totale=rischio.esposizione_totale,
            accordato_totale=rischio.accordato_totale,
            esposizione_in_sofferenza=rischio.esposizione_in_sofferenza,
            posizioni=posizioni_dto,
        )
