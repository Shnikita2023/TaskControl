from datetime import date
from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class ProductCreate(BaseModel):
    code_product: str = Field(validation_alias="УникальныйКодПродукта")
    party_number: int = Field(validation_alias="НомерПартии")
    party_date: date = Field(validation_alias="ДатаПартии")


class ProductShow(BaseModel):
    id: int
    part_id: int
    code_product: str
    is_aggregated: bool
    aggregated_at: datetime | None
