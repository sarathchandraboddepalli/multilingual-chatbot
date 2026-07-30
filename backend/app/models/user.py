import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Boolean, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class ChatUser(Base):
    __tablename__ = "chat_users"
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    phone: Mapped[str | None] = mapped_column(String(15), unique=True)
    name: Mapped[str | None] = mapped_column(String(255))
    preferred_language: Mapped[str] = mapped_column(String(10), default="en")
    district: Mapped[str | None] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
