"""Implementazione in-memory del PosizioneCrediziziaRepository."""
from __future__ import annotations

from typing import Dict, List, Optional
from uuid import UUID

from src.domain.entities.posizione_creditizia import PosizioneCredizizia
from src.domain.repositories.posizione_creditizia_repository import (
    PosizioneCrediziziaRepository,
)


class InMemoryPosizioneCrediziziaRepository(PosizioneCrediziziaRepository):
    """Repository in-memory delle Posizioni Creditizie, adatto per test e prototipazione."""

    def __init__(self) -> None:
        self._store: Dict[UUID, PosizioneCredizizia] = {}

    def salva(self, posizione: PosizioneCredizizia) -> None:
        self._store[posizione.id] = posizione

    def trova_per_id(self, id: UUID) -> Optional[PosizioneCredizizia]:
        return self._store.get(id)

    def trova_per_soggetto(self, soggetto_id: UUID) -> List[PosizioneCredizizia]:
        return [p for p in self._store.values() if p.soggetto_id == soggetto_id]

    def elimina(self, id: UUID) -> None:
        self._store.pop(id, None)
