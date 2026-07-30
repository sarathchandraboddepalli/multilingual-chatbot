from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class ConversationCreate(BaseModel):
    channel: str = "web"
    language: str = "en"


class ConversationOut(BaseModel):
    id: UUID
    channel: str
    language: str
    status: str
    created_at: datetime
    model_config = {"from_attributes": True}
