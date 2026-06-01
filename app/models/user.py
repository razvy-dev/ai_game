import uuid
import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Text, DateTime, func

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False, unique=False)
    phone: Mapped[str | None] = mapped_column(String(255), nullable=True, unique=True)
    image: Mapped[str | None] = mapped_column(
        String(255),
        nullable = True,
        default = None,
    )
    ip: Mapped[str | None] = mapped_column(
        String(255),
        nullable = True,
        default = None
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # TODO: implement user image