from pydantic import BaseModel
from uuid import UUID


class SchemeCreate(BaseModel):
    scheme_id: str
    name: str
    name_telugu: str | None = None
    description: str
    eligibility: str | None = None
    benefits: str | None = None
    documents_required: str | None = None
    application_url: str | None = None
    department: str | None = None
    category: str | None = None


class SchemeOut(BaseModel):
    id: UUID
    scheme_id: str
    name: str
    description: str
    category: str | None
    is_active: bool
    model_config = {"from_attributes": True}
