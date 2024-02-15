from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime

from app.api_v1.products.schemas import ProductShow
from app.db.database import Base


class Product(Base):
    """Модель продукции"""
    __tablename__ = "product"

    code_product: Mapped[str] = mapped_column(unique=True)
    is_aggregated: Mapped[bool] = mapped_column(default=False)
    aggregated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    party_id: Mapped[int] = mapped_column(ForeignKey(column="party.id", ondelete="CASCADE"))
    party = relationship("Party", back_populates="products")

    def to_read_model(self) -> ProductShow:
        return ProductShow(
            id=self.id,
            part_id=self.party_id,
            code_product=self.code_product,
            is_aggregated=self.is_aggregated,
            aggregated_at=self.aggregated_at
        )
