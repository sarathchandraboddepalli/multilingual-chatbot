import uuid
from datetime import datetime
from sqlalchemy import String, Text, DateTime, Boolean, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Scheme(Base):
    __tablename__ = "schemes"
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    scheme_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    name_telugu: Mapped[str | None] = mapped_column(String(500))
    description: Mapped[str] = mapped_column(Text, nullable=False)
    eligibility: Mapped[str | None] = mapped_column(Text)
    benefits: Mapped[str | None] = mapped_column(Text)
    documents_required: Mapped[str | None] = mapped_column(Text)
    application_url: Mapped[str | None] = mapped_column(String(1024))
    department: Mapped[str | None] = mapped_column(String(255))
    category: Mapped[str | None] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
