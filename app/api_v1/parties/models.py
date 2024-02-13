from datetime import date, datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Party(Base):
    """Модель партии"""
    __tablename__ = "party"

    status_closed: Mapped[bool]
    closed_at: Mapped[datetime | None] = mapped_column(default=None)
    task_description: Mapped[str]
    line: Mapped[str]
    shift: Mapped[str]
    brigade: Mapped[str]
    party_number: Mapped[int] = mapped_column(unique=True)
    party_date: Mapped[date] = mapped_column(unique=True)
    nomenclature: Mapped[str]
    ecn_code: Mapped[str]
    rc_identifier: Mapped[str]
    shift_start_datetime: Mapped[datetime]
    shift_end_datetime: Mapped[datetime]

    product = relationship("Product", back_populates="party", uselist=False)
