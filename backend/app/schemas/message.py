from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class ChatRequest(BaseModel):
    conversation_id: UUID | None = None
    message: str
    language: str = "en"


class ChatResponse(BaseModel):
    conversation_id: UUID
    response: str
    language: str
    scheme_referenced: str | None = None
    confidence_score: float | None = None


class MessageOut(BaseModel):
    id: UUID
    role: str
    content: str
    language: str
    created_at: datetime
    model_config = {"from_attributes": True}
