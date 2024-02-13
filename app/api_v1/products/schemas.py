from datetime import date

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    code_product: str = Field(validation_alias="УникальныйКодПродукта")
    party_number: int = Field(validation_alias="НомерПартии")
    party_date: date = Field(validation_alias="ДатаПартии")




