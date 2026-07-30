import pytest


@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_list_conversations_empty(client):
    response = await client.get("/api/v1/conversations/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_list_schemes_empty(client):
    response = await client.get("/api/v1/schemes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_add_scheme(client):
    response = await client.post("/api/v1/schemes/", json={
        "scheme_id": "TEST-001",
        "name": "Test Scheme",
        "description": "A test scheme for unit testing",
        "category": "test",
    })
    assert response.status_code == 200
    assert response.json()["scheme_id"] == "TEST-001"


@pytest.mark.asyncio
async def test_chat_endpoint(client):
    response = await client.post("/api/v1/chat/", json={
        "message": "tell me about pension schemes",
        "language": "en"
    })
    assert response.status_code == 200
    data = response.json()
    assert "conversation_id" in data
    assert "response" in data
    assert len(data["response"]) > 0
