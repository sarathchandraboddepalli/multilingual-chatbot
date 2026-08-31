# Mana Mitra — Multilingual Government Services Chatbot

A WhatsApp-first chatbot that answers citizen queries about government schemes in Telugu, Hindi, and English. Built for Andhra Pradesh but extensible to any state. Uses Bhashini (India's national language translation API) for language detection and translation, and Claude Haiku for response generation over a RAG-indexed scheme knowledge base.

**Mana Mitra** means "Our Friend" in Telugu.

## The Problem It Solves

Crores of citizens in Andhra Pradesh are eligible for schemes like YSR Pension Kanuka, Rythu Bharosa, and Aarogyasri but don't know eligibility criteria, required documents, or application URLs — and they can't navigate English-language government portals. This bot meets them on WhatsApp in their own language.

## Architecture

```
Citizen (WhatsApp / Web)
         |
         v
   Meta Webhooks / Web Frontend (port 3002)
         |
         v
   FastAPI (port 8002)
         |
   ------+--------+----------+
   |              |          |
   v              v          v
PostgreSQL   Bhashini API  Anthropic
(conversations, (translation)  Claude Haiku
 schemes)                   (generation)
         |
         v
   In-memory RAG index
   (keyword-matched scheme store)
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | FastAPI 0.115, Python 3.12 |
| LLM | Anthropic Claude Haiku |
| Translation | Bhashini API (Government of India NLP platform) |
| Database | PostgreSQL 16 + SQLAlchemy (async) + Alembic |
| Frontend | Next.js 14, Tailwind CSS |
| Messaging | Meta WhatsApp Business API (webhook) |
| Containerisation | Docker + Docker Compose |

## Supported Languages

| Language | Code | Detection |
|----------|------|-----------|
| Telugu | te | Bhashini auto-detect |
| Hindi | hi | Bhashini auto-detect |
| English | en | Default fallback |

Language is detected per-message, not per-session — citizens can switch languages mid-conversation.

## Scheme Knowledge Base

Five schemes seeded by default:

| Scheme | Benefits |
|--------|---------|
| YSR Pension Kanuka | Rs. 2,750-3,000/month for elderly, disabled, widows |
| YSR Rythu Bharosa | Rs. 13,500/year for farmer families |
| YSR Aarogyasri | Free health cover up to Rs. 5 lakh/year for BPL families |
| PM Kisan Samman Nidhi | Rs. 6,000/year for small and marginal farmers |
| PM Awas Yojana Gramin | Rs. 1.2-1.3 lakh for rural BPL house construction |

New schemes are added through the admin panel or directly via the API — no redeploy needed.

## Features

- **Multilingual RAG** — query translated to English, matched against scheme index, response generated and translated back to the user's language
- **Conversation history** — last 10 messages used as context for follow-up questions
- **WhatsApp webhook** — Meta Business API-compatible endpoint with signature verification
- **Confidence scoring** — responses include a confidence score based on RAG match quality
- **Fallback responses** — if Claude API is unavailable, returns best-matched scheme context directly
- **Admin dashboard** — view all conversations, add/edit schemes, browse the knowledge base

## Quick Start

```bash
git clone https://github.com/sarathchandraboddepalli/multilingual-chatbot
cd multilingual-chatbot
cp .env.example .env    # add ANTHROPIC_API_KEY, BHASHINI_API_KEY, WHATSAPP_VERIFY_TOKEN
docker-compose up --build
```

Run migrations:
```bash
docker-compose exec api alembic upgrade head
```

- **Chat UI:** http://localhost:3002
- **API:** http://localhost:8002
- **Admin:** http://localhost:3002/admin
- **Swagger docs:** http://localhost:8002/docs

## API Reference

```
POST /api/v1/chat/                   # Send a message (web channel)
POST /api/v1/webhook/                # WhatsApp webhook endpoint
GET  /api/v1/conversations/          # List all conversations (admin)
GET  /api/v1/schemes/                # List all schemes
POST /api/v1/schemes/                # Add a new scheme
```

### Chat Request

```json
{
  "message": "YSR pension ki apply cheyyadam ela?",
  "language": "te",
  "conversation_id": null
}
```

### Chat Response

```json
{
  "conversation_id": "uuid",
  "response": "YSR Pension Kanuka ki apply cheyyadaniki...",
  "language": "te",
  "scheme_referenced": "YSR-PENSION",
  "confidence_score": 0.85
}
```

## Running Tests

```bash
cd backend
pip install pytest pytest-asyncio anyio httpx aiosqlite fastapi pydantic pydantic-settings "sqlalchemy[asyncio]" anthropic numpy
python -m pytest tests/ -v
```

## Environment Variables

| Variable | Description |
|----------|-------------|
|  | PostgreSQL connection string |
|  | Anthropic API key |
|  | Bhashini translation API key |
|  | WhatsApp webhook verification token |

## Extending to Other States

1. Add schemes via the admin panel or seed script
2. Set  to unlock additional regional languages (Bhashini supports 22 scheduled languages)
3. Update the system prompt in  with your state name
