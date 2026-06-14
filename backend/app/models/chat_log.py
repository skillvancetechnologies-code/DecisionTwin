"""Per-session chat history for multi-turn copilot memory."""
import uuid

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ChatMessage(Base, TimestampMixin):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_session_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, index=True)
    role: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    related_sim_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("scenarios.id", ondelete="SET NULL"), nullable=True
    )
