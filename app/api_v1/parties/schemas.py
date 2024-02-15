from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.api_v1.products.schemas import ProductShow


class PartyCreate(BaseModel):
    status_closed: bool = Field(validation_alias="СтатусЗакрытия")
    task_description: str = Field(validation_alias="ПредставлениеЗаданияНаСмену")
    line: str = Field(validation_alias="Линия")
    shift: str = Field(validation_alias="Смена")
    brigade: str = Field(validation_alias="Бригада")
    party_number: int = Field(validation_alias="НомерПартии")
    party_date: date = Field(validation_alias="ДатаПартии")
    nomenclature: str = Field(validation_alias="Номенклатура")
    ecn_code: str = Field(validation_alias="КодЕКН")
    rc_identifier: str = Field(validation_alias="ИдентификаторРЦ")
    shift_start_datetime: datetime = Field(validation_alias="ДатаВремяНачалаСмены")
    shift_end_datetime: datetime = Field(validation_alias="ДатаВремяОкончанияСмены")


class PartyShow(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
    status_closed: bool
    closed_at: Optional[datetime]
    task_description: str
    line: str
    shift: str
    brigade: str
    party_number: int
    party_date: date
    nomenclature: str
    ecn_code: str
    rc_identifier: str
    shift_start_datetime: datetime
    shift_end_datetime: datetime
    products: list[ProductShow]


class PartyUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status_closed: Optional[bool] = Field(default=None)
    task_description: Optional[str] = Field(default=None)
    line: Optional[str] = Field(default=None)
    shift: Optional[str] = Field(default=None)
    brigade: Optional[str] = Field(default=None)
    party_number: Optional[int] = Field(default=None)
    party_date: Optional[date] = Field(default=None)
    nomenclature: Optional[str] = Field(default=None)
    ecn_code: Optional[str] = Field(default=None)
    rc_identifier: Optional[str] = Field(default=None)
    shift_start_datetime: Optional[datetime] = Field(default=None)
    shift_end_datetime: Optional[datetime] = Field(default=None)

