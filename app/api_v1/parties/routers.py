from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api_v1.parties.schemas import PartyCreate, PartyShow, PartyUpdate
from app.api_v1.parties.services import party_service
from app.api_v1.parties.utils import check_type_value_party
from app.db.database import get_async_session

router_party = APIRouter(prefix="/parties", tags=["Parties"])


@router_party.post(
    path="/", summary="Создание сменного задание", status_code=status.HTTP_201_CREATED
)
async def create_party(
    parties: list[PartyCreate], session: AsyncSession = Depends(get_async_session)
) -> dict:
    return await party_service.add_party(session=session, parties=parties)


@router_party.get(
    path="/{party_id}", summary="Получение сменного задание", response_model=PartyShow
)
async def get_party(
    party_id: int, session: AsyncSession = Depends(get_async_session)
) -> PartyShow:
    return await party_service.get_party(session=session, party_id=party_id)


@router_party.patch(
    path="/{party_id}",
    summary="Обновление сменного задание",
    response_model=PartyUpdate,
)
async def update_party(
    party_id: int,
    new_party: PartyUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> PartyUpdate:
    return await party_service.update_party(
        session=session, new_party=new_party, party_id=party_id
    )


@router_party.get(path="/", summary="Получение сменных заданий по различным фильтрам")
async def get_parties_by_filter(
    value_party: str = Depends(check_type_value_party),
    offset: int = Query(ge=0, default=0),
    limit: int = Query(ge=1, default=1),
    name_party: str = "party_number",
    session: AsyncSession = Depends(get_async_session),
) -> list[dict[str, Any]]:
    return await party_service.get_parties_by_filter(
        session=session,
        name_party=name_party,
        value_party=value_party,
        offset=offset,
        limit=limit,
    )
