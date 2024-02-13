from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.db.database import Base


class Product(Base):
    """Модель продукции"""
    __tablename__ = "product"

    code_product: Mapped[str] = mapped_column(unique=True)
    is_aggregated: Mapped[bool]
    aggregated_at: Mapped[datetime]

    party_id: Mapped[int] = mapped_column(ForeignKey(column="party_id"), unique=True)
    party = relationship("Party", back_populates="product")
