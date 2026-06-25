"""Dependency injection per FastAPI."""
from __future__ import annotations

from src.infrastructure.repositories.in_memory_soggetto_repository import (
    InMemorySoggettoRepository,
)
from src.infrastructure.repositories.in_memory_posizione_creditizia_repository import (
    InMemoryPosizioneCreditiziaRepository,
)
from src.application.use_cases.soggetto_service import SoggettoService
from src.application.use_cases.centrale_rischi_service import CentraleRischiService

# Repository condivisi (singleton per l'intera applicazione)
_soggetto_repo = InMemorySoggettoRepository()
_posizione_repo = InMemoryPosizioneCreditiziaRepository()


def get_soggetto_service() -> SoggettoService:
    return SoggettoService(_soggetto_repo)


def get_centrale_rischi_service() -> CentraleRischiService:
    return CentraleRischiService(_soggetto_repo, _posizione_repo)
