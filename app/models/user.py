import uuid
import datetime

from app.database import Base

class Issue(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False, unique=False)
    phone: Mapped[str | None] = mapped_column(String(255), nullable=True, unique=True)
    image: Mapped[str | None] = mapped_column(
        String(255),
        nullable = True,
        default = None,
    )

    # TODO: implement user image