"""Router FastAPI per i Soggetti."""
from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.dtos.soggetto_dto import CreaSoggettoCommand
from src.application.use_cases.soggetto_service import SoggettoService
from src.presentation.schemas.soggetto_schema import CreaSoggettoRequest, SoggettoResponse
from src.presentation.api.dependencies import get_soggetto_service

router = APIRouter(prefix="/soggetti", tags=["Soggetti"])


@router.post(
    "/",
    response_model=SoggettoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Censisce un nuovo Soggetto",
)
def crea_soggetto(
    body: CreaSoggettoRequest,
    service: SoggettoService = Depends(get_soggetto_service),
) -> SoggettoResponse:
    try:
        dto = service.crea_soggetto(
            CreaSoggettoCommand(
                codice_fiscale=body.codice_fiscale,
                denominazione=body.denominazione,
                natura_giuridica=body.natura_giuridica,
                partita_iva=body.partita_iva,
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return SoggettoResponse(**dto.__dict__)


@router.get(
    "/",
    response_model=List[SoggettoResponse],
    summary="Elenco di tutti i Soggetti censiti",
)
def lista_soggetti(
    service: SoggettoService = Depends(get_soggetto_service),
) -> List[SoggettoResponse]:
    return [SoggettoResponse(**s.__dict__) for s in service.lista_soggetti()]


@router.get(
    "/{soggetto_id}",
    response_model=SoggettoResponse,
    summary="Dettaglio di un Soggetto",
)
def ottieni_soggetto(
    soggetto_id: UUID,
    service: SoggettoService = Depends(get_soggetto_service),
) -> SoggettoResponse:
    dto = service.ottieni_soggetto(soggetto_id)
    if dto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Soggetto '{soggetto_id}' non trovato.",
        )
    return SoggettoResponse(**dto.__dict__)


@router.delete(
    "/{soggetto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Elimina un Soggetto",
)
def elimina_soggetto(
    soggetto_id: UUID,
    service: SoggettoService = Depends(get_soggetto_service),
) -> None:
    try:
        service.elimina_soggetto(soggetto_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
