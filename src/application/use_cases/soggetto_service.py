"""Use case: gestione dei Soggetti censiti nella Centrale Rischi."""
from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from src.domain.entities.soggetto import Soggetto
from src.domain.repositories.soggetto_repository import SoggettoRepository
from src.application.dtos.soggetto_dto import CreaSoggettoCommand, SoggettoDTO


def _to_dto(soggetto: Soggetto) -> SoggettoDTO:
    return SoggettoDTO(
        id=soggetto.id,
        codice_fiscale=soggetto.codice_fiscale,
        denominazione=soggetto.denominazione,
        natura_giuridica=soggetto.natura_giuridica,
        partita_iva=soggetto.partita_iva,
    )


class SoggettoService:
    """Orchestrazione dei casi d'uso relativi ai Soggetti."""

    def __init__(self, soggetto_repo: SoggettoRepository) -> None:
        self._repo = soggetto_repo

    def crea_soggetto(self, command: CreaSoggettoCommand) -> SoggettoDTO:
        """Crea e persiste un nuovo Soggetto."""
        esistente = self._repo.trova_per_codice_fiscale(command.codice_fiscale)
        if esistente is not None:
            raise ValueError(
                f"Soggetto con codice fiscale '{command.codice_fiscale}' già presente."
            )
        soggetto = Soggetto(
            codice_fiscale=command.codice_fiscale,
            denominazione=command.denominazione,
            natura_giuridica=command.natura_giuridica,
            partita_iva=command.partita_iva,
        )
        self._repo.salva(soggetto)
        return _to_dto(soggetto)

    def ottieni_soggetto(self, id: UUID) -> Optional[SoggettoDTO]:
        """Ritorna il DTO del Soggetto con l'id indicato, oppure None."""
        soggetto = self._repo.trova_per_id(id)
        return _to_dto(soggetto) if soggetto else None

    def cerca_per_codice_fiscale(self, codice_fiscale: str) -> Optional[SoggettoDTO]:
        """Ricerca un Soggetto tramite codice fiscale."""
        soggetto = self._repo.trova_per_codice_fiscale(codice_fiscale)
        return _to_dto(soggetto) if soggetto else None

    def lista_soggetti(self) -> List[SoggettoDTO]:
        """Ritorna la lista di tutti i Soggetti."""
        return [_to_dto(s) for s in self._repo.lista_tutti()]

    def elimina_soggetto(self, id: UUID) -> None:
        """Elimina un Soggetto per id."""
        if self._repo.trova_per_id(id) is None:
            raise ValueError(f"Soggetto con id '{id}' non trovato.")
        self._repo.elimina(id)
