# Mana Mitra — Multilingual Government Services Chatbot

A WhatsApp/web chatbot that answers citizen queries about government schemes in **Telugu, Hindi, and English**. Built with FastAPI, Next.js, and the Anthropic Claude API.

## Quick Start

```bash
# Clone and configure
cp .env.example .env
# Set ANTHROPIC_API_KEY in .env

# Start with Docker
docker-compose up --build

# First-time: run migrations
docker-compose exec api alembic upgrade head
```

- Frontend: http://localhost:3002
- API: http://localhost:8002
- Swagger docs: http://localhost:8002/docs

## Run Tests (no Docker needed)

```bash
cd backend
pip install pytest pytest-asyncio anyio httpx aiosqlite fastapi pydantic pydantic-settings "sqlalchemy[asyncio]" anthropic
python -m pytest tests/ -v
```

## Features

- Chat in Telugu, Hindi, or English
- RAG retrieval over 5 seeded AP/India government schemes
- Admin dashboard: view conversations, add schemes to knowledge base
- WhatsApp webhook skeleton (Meta Business API format)
- Fallback responses when Claude API is unavailable

See [CHANGES.md](CHANGES.md) for full documentation.
