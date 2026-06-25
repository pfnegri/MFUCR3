"""Interfaccia del repository per le Posizioni Creditizie."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.entities.posizione_creditizia import PosizioneCredizizia


class PosizioneCrediziziaRepository(ABC):
    """Porta di uscita del dominio per la persistenza delle Posizioni Creditizie."""

    @abstractmethod
    def salva(self, posizione: PosizioneCredizizia) -> None:
        """Persiste una nuova Posizione Creditizia o aggiorna quella esistente."""

    @abstractmethod
    def trova_per_id(self, id: UUID) -> Optional[PosizioneCredizizia]:
        """Ritorna la Posizione con l'id indicato, oppure None."""

    @abstractmethod
    def trova_per_soggetto(self, soggetto_id: UUID) -> List[PosizioneCredizizia]:
        """Ritorna tutte le posizioni del soggetto indicato."""

    @abstractmethod
    def elimina(self, id: UUID) -> None:
        """Rimuove la Posizione con l'id indicato."""
