"""Interfaccia del repository per i Soggetti."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.entities.soggetto import Soggetto


class SoggettoRepository(ABC):
    """Porta di uscita del dominio per la persistenza dei Soggetti."""

    @abstractmethod
    def salva(self, soggetto: Soggetto) -> None:
        """Persiste un nuovo Soggetto o aggiorna quello esistente."""

    @abstractmethod
    def trova_per_id(self, id: UUID) -> Optional[Soggetto]:
        """Ritorna il Soggetto con l'id indicato, oppure None."""

    @abstractmethod
    def trova_per_codice_fiscale(self, codice_fiscale: str) -> Optional[Soggetto]:
        """Ritorna il Soggetto con il codice fiscale indicato, oppure None."""

    @abstractmethod
    def lista_tutti(self) -> List[Soggetto]:
        """Ritorna la lista di tutti i Soggetti censiti."""

    @abstractmethod
    def elimina(self, id: UUID) -> None:
        """Rimuove il Soggetto con l'id indicato."""
