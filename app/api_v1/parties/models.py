from datetime import date, datetime

from sqlalchemy import DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api_v1.parties.schemas import PartyShow
from app.db.database import Base


class Party(Base):
    """Модель партии"""
    __tablename__ = "party"

    status_closed: Mapped[bool]
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    task_description: Mapped[str]
    line: Mapped[str]
    shift: Mapped[str]
    brigade: Mapped[str]
    party_number: Mapped[int]
    party_date: Mapped[date]
    nomenclature: Mapped[str]
    ecn_code: Mapped[str]
    rc_identifier: Mapped[str]
    shift_start_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    shift_end_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    products = relationship("Product", back_populates="party")

    UniqueConstraint("party_number", "party_date", name="party_number_date")

    def to_read_model(self) -> PartyShow:
        products = [product.to_read_model() for product in self.products]
        return PartyShow(
            id=self.id,
            status_closed=self.status_closed,
            closed_at=self.closed_at,
            task_description=self.task_description,
            line=self.line,
            shift=self.shift,
            brigade=self.brigade,
            party_number=self.party_number,
            party_date=self.party_date,
            nomenclature=self.nomenclature,
            ecn_code=self.ecn_code,
            rc_identifier=self.rc_identifier,
            shift_start_datetime=self.shift_start_datetime,
            shift_end_datetime=self.shift_end_datetime,
            products=products
        )
