from datetime import datetime
from typing import Any

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.parties.models import Party
from app.api_v1.parties.repository import PartyRepository
from app.api_v1.parties.schemas import PartyCreate, PartyShow, PartyUpdate


class PartyService:
    """Cервис для работы с партиями"""

    @classmethod
    async def _prepary_party_data(cls,
                                  session: AsyncSession,
                                  parties: list[PartyCreate]) -> tuple[list[Party], list[dict]]:
        """Подготовка данных для добавления и обновление партий"""
        list_party_add = []
        list_party_update = []
        for party in parties:
            party_dict: dict = party.model_dump()

            params_party: dict = {
                "party_number": party_dict["party_number"],
                "party_date": party_dict["party_date"]
            }

            existing_model_party: Party | None = await cls.check_existing_model_party(session=session,
                                                                                      params_party=params_party)

            if party.status_closed:
                party_dict.update(closed_at=datetime.utcnow())

            if existing_model_party:
                party_dict.update(id=existing_model_party.id)
                list_party_update.append(party_dict)

            else:
                list_party_add.append(Party(**party_dict))

        return list_party_add, list_party_update

    @classmethod
    async def add_party(cls, session: AsyncSession, parties: list[PartyCreate]) -> None:
        """Добавление партии"""
        list_party_add, list_party_update = await cls._prepary_party_data(session=session, parties=parties)

        if list_party_add:
            await PartyRepository(session=session).add_all(data=list_party_add)

        if list_party_update:
            await PartyRepository(session=session).update_all(data=list_party_update)

        return None

    @staticmethod
    async def check_existing_model_party(session: AsyncSession, params_party: dict) -> Party | None:
        """Проверка существующей модели партии"""
        return await PartyRepository(session=session).find_one_by_params(**params_party)

    @staticmethod
    async def get_party(session: AsyncSession, party_id: int) -> PartyShow:
        """Получение партии со связанной продукции"""
        existing_model_party: None | Party = await PartyRepository(session=session).find_one_by_join(party_id=party_id)

        if not existing_model_party:
            raise HTTPException(status_code=404, detail="not found id party")

        return existing_model_party.to_read_model()

    @classmethod
    async def update_party(cls, session: AsyncSession, new_party: PartyUpdate, party_id: int) -> PartyUpdate:
        """Обновление партии со связанной продукции"""

        existing_model_party: Party | None = await PartyRepository(session=session).find_one(id_data=party_id)

        if not existing_model_party:
            raise HTTPException(status_code=404, detail="not found id party")

        updated_party_dict: dict[str, Any] = new_party.dict(exclude_none=True)

        if updated_party_dict["status_closed"]:
            updated_party_dict.update(closed_at=datetime.utcnow())

        else:
            updated_party_dict.update(closed_at=None)

        updated_party_model: Party = await PartyRepository(session=session).update_one(id_data=party_id,
                                                                                       new_data=updated_party_dict)
        schemas_party: PartyUpdate = PartyUpdate.from_orm(updated_party_model)

        return schemas_party

    @staticmethod
    async def get_parties_by_filter(session: AsyncSession,
                                    name_party: str,
                                    value_party: Any,
                                    offset: int,
                                    limit: int) -> list[dict[str, Any]]:
        """Получение партий со связанной продукции по фильтрам"""
        list_models: list[dict[str, Any]] = (await PartyRepository(session=session).
                                             find_all_by_param(param_column=name_party,
                                                               value=value_party,
                                                               offset=offset,
                                                               limit=limit))

        return list_models


party_service: PartyService = PartyService()
