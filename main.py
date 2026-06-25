"""Entry point dell'applicazione Centrale Rischi."""
from fastapi import FastAPI

from src.presentation.api.soggetti_router import router as soggetti_router
from src.presentation.api.centrale_rischi_router import router as centrale_rischi_router

app = FastAPI(
    title="Centrale Rischi",
    description="API per la gestione della Centrale Rischi con architettura a strati.",
    version="1.0.0",
)

app.include_router(soggetti_router)
app.include_router(centrale_rischi_router)
