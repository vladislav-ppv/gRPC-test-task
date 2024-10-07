from datetime import datetime
from typing import Optional

from sqlalchemy import CheckConstraint, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from line_provider.app.schemas.event import StatusEnum
from line_provider.app.schemas.score import ScoreStatusEnum


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


class ScoreModel(Base):
    __tablename__ = "scores"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    event_id: Mapped[int]
    rate: Mapped[int] = mapped_column(CheckConstraint('rate >= 1 AND rate <= 100', name='check_rate_range'))
    status: Mapped[ScoreStatusEnum] = mapped_column(server_default=ScoreStatusEnum.mutable.name)

    def __repr__(self) -> str:
        return f"Score(id={self.id!r}, rate={self.rate!r}, status={self.status!r})"
