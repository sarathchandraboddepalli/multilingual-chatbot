# Multilingual Government Services Chatbot — CHANGES

## What Was Built

A production-ready MVP for a multilingual government services chatbot targeting citizens of Andhra Pradesh. The system answers queries about government welfare schemes in Telugu, Hindi, and English using RAG (Retrieval-Augmented Generation) with in-memory vector search and the Anthropic Claude API.

### Architecture Overview

- **Backend**: FastAPI (Python 3.12) with async SQLAlchemy, PostgreSQL via asyncpg, Alembic migrations
- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS
- **RAG**: In-memory keyword-based retrieval (production upgrade path: Qdrant + embeddings)
- **Translation**: Bhashini API mock (production upgrade path: Dhruva API)
- **LLM**: Anthropic Claude Haiku via the `anthropic` Python SDK
- **WhatsApp**: Meta Business API webhook integration skeleton
- **Containerisation**: Docker + Docker Compose (Postgres 16, FastAPI, Next.js)

---

## API Endpoints

All backend routes are prefixed with `/api/v1`.

### Chat
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/chat/` | Send a message, get an AI response with scheme context |

**Request body:**
```json
{
  "message": "How do I apply for YSR Pension?",
  "language": "en",
  "conversation_id": null
}
```

**Response:**
```json
{
  "conversation_id": "<uuid>",
  "response": "To apply for YSR Pension Kanuka...",
  "language": "en",
  "scheme_referenced": "YSR Pension Kanuka",
  "confidence_score": 0.85
}
```

### Conversations
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/conversations/` | List last 50 conversations |
| GET | `/api/v1/conversations/{id}/messages` | Get all messages in a conversation |

### Schemes (Knowledge Base)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/schemes/` | List all active schemes |
| POST | `/api/v1/schemes/` | Add a new scheme to the knowledge base |
| GET | `/api/v1/schemes/{scheme_id}` | Get a specific scheme by ID |

### WhatsApp Webhook
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/webhook/whatsapp` | Meta webhook verification (hub.challenge) |
| POST | `/api/v1/webhook/whatsapp` | Receive inbound WhatsApp messages |

### Health
| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check — returns `{"status": "ok"}` |

---

## Key Files

### Backend (`backend/`)
- `app/main.py` — FastAPI app, CORS middleware, router registration
- `app/config.py` — Pydantic Settings, reads from `.env`
- `app/database.py` — Async SQLAlchemy engine and session factory
- `app/models/` — ORM models: ChatUser, Conversation, Message, Scheme
- `app/schemas/` — Pydantic schemas for request/response validation
- `app/services/chat_service.py` — Core chat flow: language detection → RAG retrieval → Claude API → persist
- `app/services/rag_service.py` — In-memory keyword RAG, `seed_default_schemes()` with 5 AP/India schemes
- `app/services/translation_service.py` — Bhashini mock: detects Telugu/Hindi via Unicode ranges, returns `[LANG] text`
- `app/services/scheme_service.py` — DB CRUD + RAG index updates for schemes
- `app/api/v1/` — Route handlers: chat, conversations, schemes, webhook
- `alembic/` — Migration scripts for all 4 tables
- `tests/` — 10 pytest tests (5 RAG unit tests + 5 API integration tests)

### Frontend (`frontend/`)
- `src/app/layout.tsx` — Root layout with nav bar (Mana Mitra branding, green theme)
- `src/app/chat/page.tsx` — Chat UI: message bubbles, language selector, conversation continuity
- `src/app/admin/page.tsx` — Dashboard: conversation count, active scheme count
- `src/app/admin/conversations/page.tsx` — Browse conversations + message viewer
- `src/app/admin/schemes/page.tsx` — Add/view schemes table
- `src/lib/api.ts` — Typed fetch wrapper for all backend endpoints
- `src/lib/utils.ts` — `formatTime()`, `LANGUAGES` constant

### Root
- `docker-compose.yml` — Three services: `api` (8002), `frontend` (3002), `db` (5434)
- `.env.example` — Template for environment variables
- `alembic.ini` — Alembic migration config

---

## Seeded Knowledge Base (5 Default Schemes)

| Scheme ID | Name | Benefit |
|-----------|------|---------|
| YSR-PENSION | YSR Pension Kanuka | Rs 2750–3000/month for elderly, disabled, widows |
| YSR-RYTHU-BHAROSA | YSR Rythu Bharosa | Rs 13,500/year to farmer families |
| YSR-AAROGYASRI | YSR Aarogyasri | Free health insurance up to Rs 5 lakh/year |
| PM-KISAN | PM Kisan Samman Nidhi | Rs 6000/year to small/marginal farmers |
| PMAY-GRAMIN | PMAY Gramin | Rs 1.20–1.30 lakh for rural house construction |

---

## How to Run with Docker

```bash
# 1. Copy and fill in your credentials
cp .env.example .env
# Edit .env: set ANTHROPIC_API_KEY, optionally change DB_PASSWORD

# 2. Start all services
docker-compose up --build

# 3. Run database migrations (first time only)
docker-compose exec api alembic upgrade head

# Backend API: http://localhost:8002
# Frontend UI: http://localhost:3002
# API docs (Swagger): http://localhost:8002/docs
```

---

## How to Run Tests

```bash
cd backend

# Install dependencies (one-time)
pip install pytest pytest-asyncio anyio httpx aiosqlite \
  fastapi pydantic pydantic-settings "sqlalchemy[asyncio]" anthropic

# Run all tests
python -m pytest tests/ -v
```

Expected output: **10 passed** in ~1 second. Tests use SQLite in-memory (no Postgres required). The chat test works without a real Anthropic API key because `chat_service.py` has a fallback response when the API call fails.

---

## Next Steps for an AI Agent

1. **Real Embeddings**: Replace keyword RAG in `rag_service.py` with sentence-transformers + Qdrant for semantic search. The `search_schemes()` and `index_scheme()` function signatures are already the right interface.

2. **Real Translation**: Implement `translate_text()` and `detect_language()` in `translation_service.py` using the Bhashini Dhruva API (`POST https://dhruva-api.bhashini.gov.in/services/inference/pipeline`). The mock already returns the correct shape.

3. **WhatsApp Send**: In `webhook.py`, after generating a response, call the Meta Graph API to send the reply back to the user's WhatsApp number. Add `WHATSAPP_ACCESS_TOKEN` and `WHATSAPP_PHONE_NUMBER_ID` to config.

4. **Authentication**: Add JWT-based auth to the admin endpoints (`/conversations`, `/schemes`). Use `fastapi-users` or a simple `Depends(verify_token)` guard.

5. **Vector DB Upgrade**: Replace the `_scheme_index` dict with Qdrant collections. Run Qdrant as a fourth Docker service. Add `qdrant-client` to requirements.

6. **Telemetry**: Add OpenTelemetry tracing to `chat_service.py` to measure LLM latency, RAG hit rate, and language distribution.

7. **Scheme Import**: Add a bulk import endpoint `POST /api/v1/schemes/bulk` that accepts a JSON array, for seeding the knowledge base from official government data dumps.

8. **CI/CD**: Add a `.github/workflows/test.yml` that runs `pytest` on every push. The test suite is already self-contained (SQLite, no external services).
