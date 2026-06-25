"""Router FastAPI per la Centrale Rischi (posizioni e rischio credito)."""
from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.dtos.posizione_dto import CreaPosizioneCommand
from src.application.use_cases.centrale_rischi_service import CentraleRischiService
from src.presentation.schemas.posizione_schema import (
    CreaPosizioneRequest,
    PosizioneResponse,
    RischioCreditoResponse,
)
from src.presentation.api.dependencies import get_centrale_rischi_service

router = APIRouter(prefix="/centrale-rischi", tags=["Centrale Rischi"])


@router.post(
    "/posizioni",
    response_model=PosizioneResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registra una nuova posizione creditizia",
)
def registra_posizione(
    body: CreaPosizioneRequest,
    service: CentraleRischiService = Depends(get_centrale_rischi_service),
) -> PosizioneResponse:
    try:
        dto = service.registra_posizione(
            CreaPosizioneCommand(
                soggetto_id=body.soggetto_id,
                intermediario_abi=body.intermediario_abi,
                importo_accordato=body.importo_accordato,
                importo_utilizzato=body.importo_utilizzato,
                categoria_censimento=body.categoria_censimento,
                data_segnalazione=body.data_segnalazione,
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return PosizioneResponse(**dto.__dict__)


@router.get(
    "/soggetti/{soggetto_id}/posizioni",
    response_model=List[PosizioneResponse],
    summary="Elenco delle posizioni creditizie di un soggetto",
)
def posizioni_soggetto(
    soggetto_id: UUID,
    service: CentraleRischiService = Depends(get_centrale_rischi_service),
) -> List[PosizioneResponse]:
    posizioni = service.ottieni_posizioni_soggetto(soggetto_id)
    return [PosizioneResponse(**p.__dict__) for p in posizioni]


@router.get(
    "/soggetti/{soggetto_id}/rischio",
    response_model=RischioCreditoResponse,
    summary="Rischio di credito aggregato di un soggetto",
)
def rischio_soggetto(
    soggetto_id: UUID,
    service: CentraleRischiService = Depends(get_centrale_rischi_service),
) -> RischioCreditoResponse:
    dto = service.ottieni_rischio_soggetto(soggetto_id)
    if dto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Soggetto '{soggetto_id}' non trovato.",
        )
    posizioni = [PosizioneResponse(**p.__dict__) for p in dto.posizioni]
    return RischioCreditoResponse(
        soggetto_id=dto.soggetto_id,
        esposizione_totale=dto.esposizione_totale,
        accordato_totale=dto.accordato_totale,
        esposizione_in_sofferenza=dto.esposizione_in_sofferenza,
        posizioni=posizioni,
    )
