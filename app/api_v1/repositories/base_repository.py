from abc import ABC, abstractmethod
from typing import Any, Optional, Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import Result, select, update
from sqlalchemy.exc import InvalidRequestError, ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api_v1.parties.models import Party
from app.api_v1.products.models import Product


class AbstractRepository(ABC):

    @abstractmethod
    async def add_all(self, data: list):
        raise NotImplementedError

    @abstractmethod
    async def find_one_by_join(self, id_data: int, field_join: str):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, id_data: int):
        raise NotImplementedError

    @abstractmethod
    async def find_one_by_params(self, **kwargs: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_all_by_param(
        self, param_column: str, value: Any, offset: int, limit: int
    ):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id_data: int, new_data: dict[str, Any]):
        raise NotImplementedError

    @abstractmethod
    async def update_all(self, data: list[dict]):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    ModelType = Union[Product, Party]
    model: Optional[ModelType] = None
    error_500_by_bd: str = "Что-то пошло не так, попробуйте позже"
    error_400_by_type: str = "Проверьте корректность вводимых данных"

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_all(self, data: list) -> None:
        try:
            self.session.add_all(data)
            await self.session.commit()

        except ConnectionError:
            raise HTTPException(status_code=500, detail=self.error_500_by_bd)

    async def find_one_by_params(self, **kwargs: dict) -> Optional[model]:
        try:
            query = select(self.model).filter_by(**kwargs)
            result: Result = await self.session.execute(query)
            return result.scalar_one_or_none()

        except ConnectionError:
            raise HTTPException(status_code=500, detail=self.error_500_by_bd)

    async def find_all_by_param(
        self, param_column: str, value: Any, offset: int, limit: int
    ) -> list[dict[str, Any]]:
        try:
            query = (
                select(self.model)
                .filter_by(**{param_column: value})
                .offset(offset)
                .limit(limit)
            )
            result: Result = await self.session.execute(query)
            list_models: list = [jsonable_encoder(model[0]) for model in result.all()]
            return list_models

        except ConnectionError:
            raise HTTPException(status_code=500, detail=self.error_500_by_bd)

        except (ProgrammingError, InvalidRequestError):
            raise HTTPException(status_code=400, detail=self.error_400_by_type)

    async def find_one(self, id_data: int) -> Optional[model]:
        try:
            return await self.session.get(self.model, id_data)

        except ConnectionError:
            raise HTTPException(status_code=500, detail=self.error_500_by_bd)

    async def find_one_by_join(self, id_data: int, field_join: str) -> Optional[model]:
        try:
            column_join = getattr(self.model, field_join)
            query = (
                select(self.model)
                .options(selectinload(column_join))
                .where(self.model.id == id_data)
            )
            result: Result = await self.session.execute(query)
            return result.unique().scalar_one_or_none()

        except ConnectionError:
            raise HTTPException(status_code=500, detail=self.error_500_by_bd)

    async def update_one(self, id_data: int, new_data: dict[str, Any]) -> model:
        try:
            stmt = update(self.model).where(self.model.id == id_data).values(new_data)
            await self.session.execute(stmt)
            await self.session.flush()
            updated_model_orm: SQLAlchemyRepository.model = await self.session.get(
                self.model, id_data
            )
            await self.session.commit()
            return updated_model_orm

        except ConnectionError:
            raise HTTPException(status_code=500, detail=self.error_500_by_bd)

    async def update_all(self, data: list[dict]):
        try:
            await self.session.execute(update(self.model), data)
            await self.session.commit()

        except ConnectionError:
            raise HTTPException(status_code=500, detail=self.error_500_by_bd)
