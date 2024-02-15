from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api_v1.products.schemas import ProductCreate
from app.api_v1.products.services import product_service
from app.db.database import get_async_session

router_product = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router_product.post(path="/",
                     summary="Добавления продукции для сменного задания (партии)",
                     status_code=status.HTTP_201_CREATED)
async def add_product(products: list[ProductCreate],
                      session: AsyncSession = Depends(get_async_session)) -> dict:
    await product_service.add_product(session=session, products=products)
    return {"message": "the request was completed successfully"}


@router_product.get(path="/",
                    summary="Проверка агрегации продукции к партии")
async def check_aggregation_product(code_product: str,
                                    party_id: int = Query(ge=1),
                                    session: AsyncSession = Depends(get_async_session)) -> dict:
    return await product_service.check_aggregation_product(session=session,
                                                           code_product=code_product,
                                                           party_id=party_id)
