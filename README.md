# MFUCR3 – Centrale Rischi

Progetto Centrale Rischi con architettura a strati (Layered Architecture).

## Architettura

Il progetto segue un'architettura a quattro strati, ispirata ai principi del Domain-Driven Design (DDD):

```
src/
├── domain/          # Regole di business pure (entità, interfacce dei repository, domain services)
├── application/     # Orchestrazione dei casi d'uso (use cases, DTOs, comandi)
├── infrastructure/  # Implementazioni tecniche (repository in-memory, persistenza)
└── presentation/    # Layer esposto all'esterno (API REST con FastAPI, schemi Pydantic)
```

### Strati

| Strato             | Responsabilità                                                                                  |
|--------------------|-------------------------------------------------------------------------------------------------|
| **Domain**         | Entità (`Soggetto`, `PosizioneCredizizia`, `RischioCredito`), interfacce repository, domain service (`RischioCreditoService`) |
| **Application**    | Use cases (`SoggettoService`, `CentraleRischiService`), Data Transfer Objects (DTO)            |
| **Infrastructure** | Implementazioni in-memory dei repository del dominio                                           |
| **Presentation**   | Router FastAPI, schemi Pydantic per request/response, dependency injection                     |

## Requisiti

- Python 3.10+

## Installazione

```bash
pip install -r requirements.txt
```

## Avvio

```bash
uvicorn main:app --reload
```

Documentazione interattiva disponibile su: http://localhost:8000/docs

## Test

```bash
pytest tests/ -v
```
