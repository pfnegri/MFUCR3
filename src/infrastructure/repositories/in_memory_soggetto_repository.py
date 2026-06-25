"""Implementazione in-memory del SoggettoRepository."""
from __future__ import annotations

from typing import Dict, List, Optional
from uuid import UUID

from src.domain.entities.soggetto import Soggetto
from src.domain.repositories.soggetto_repository import SoggettoRepository


class InMemorySoggettoRepository(SoggettoRepository):
    """Repository in-memory dei Soggetti, adatto per test e prototipazione."""

    def __init__(self) -> None:
        self._store: Dict[UUID, Soggetto] = {}

    def salva(self, soggetto: Soggetto) -> None:
        self._store[soggetto.id] = soggetto

    def trova_per_id(self, id: UUID) -> Optional[Soggetto]:
        return self._store.get(id)

    def trova_per_codice_fiscale(self, codice_fiscale: str) -> Optional[Soggetto]:
        for soggetto in self._store.values():
            if soggetto.codice_fiscale == codice_fiscale:
                return soggetto
        return None

    def lista_tutti(self) -> List[Soggetto]:
        return list(self._store.values())

    def elimina(self, id: UUID) -> None:
        self._store.pop(id, None)
