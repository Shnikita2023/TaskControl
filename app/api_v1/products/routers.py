from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.products.schemas import ProductCreate
from app.api_v1.products.services import product_service
from app.db.database import get_async_session

router_product = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router_product.post(path="/",
                     summary="Добавления продукции для сменного задания (партии)")
async def add_product(products: list[ProductCreate],
                      session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    return await product_service.add_product(session=session, products=products)


@router_product.get(path="/",
                    summary="Проверка агрегации продукции к партии")
async def check_aggregation_product(code_product: str,
                                    party_id: int = Query(ge=1),
                                    session: AsyncSession = Depends(get_async_session)) -> dict:
    return await product_service.check_aggregation_product(session=session,
                                                           code_product=code_product,
                                                           party_id=party_id)
