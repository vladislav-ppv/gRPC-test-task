from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.schema import CheckConstraint


class Base(DeclarativeBase):
    pass


class ScoreOutboxModel(Base):
    __tablename__ = "scores_outbox"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    event_id: Mapped[int]
    rate: Mapped[int] = mapped_column(CheckConstraint('rate >= 1 AND rate <= 100', name='check_rate_range'))
    processed: Mapped[bool] = mapped_column(default=False)
    retries: Mapped[int] = mapped_column(default=0)

    def __repr__(self) -> str:
        return f"Score(id={self.id!r}, rate={self.rate!r}, processed={self.processed!r}, retries={self.retries!r})"
