from datetime import datetime
from typing import Optional

from sqlalchemy import CheckConstraint, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from line_provider.app.schemas.event import StatusEnum


class Base(DeclarativeBase):
    pass


class EventModel(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    deadline: Mapped[datetime] = mapped_column(
        CheckConstraint('deadline >= CURRENT_TIMESTAMP', name='check_deadline_range')
    )
    status: Mapped[StatusEnum] = mapped_column(server_default=StatusEnum.PROCESSING.name)

    def __repr__(self) -> str:

        return f"Event(id={self.id!r}, deadline={self.deadline!r}, status={self.status!r})"
