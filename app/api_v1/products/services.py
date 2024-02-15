from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.parties.models import Party
from app.api_v1.parties.repository import PartyRepository
from app.api_v1.parties.services import party_service
from app.api_v1.products.models import Product
from app.api_v1.products.repository import ProductRepository
from app.api_v1.products.schemas import ProductCreate


class ProductService:
    """Cервис для работы с продукции"""

    @classmethod
    async def _prepary_product_data(cls, session: AsyncSession, products: list[ProductCreate]) -> list[Product]:
        """Подготовка данных перед добавлением продукции"""
        list_products: list[Product] = []
        for product in products:
            params_party: dict = {
                "party_number": product.party_number,
                "party_date": product.party_date
            }
            existing_product: Optional[Product] = await cls._check_existing_product(session=session,
                                                                                    code_product=product.code_product)

            if existing_product:
                continue

            existing_party: Optional[Party] = await party_service.check_existing_model_party(session=session,
                                                                                             params_party=params_party)
            if existing_party:
                dict_new_product: dict = {
                    "code_product": product.code_product,
                    "party_id": existing_party.id,
                    "is_aggregated": True,
                    "aggregated_at": datetime.utcnow()
                }
                list_products.append(Product(**dict_new_product))

        return list_products

    @classmethod
    async def add_product(cls, session: AsyncSession, products: list[ProductCreate]) -> None:
        """Добавление продукции"""
        list_new_products: list[Product] = await cls._prepary_product_data(session=session, products=products)

        if list_new_products:
            await ProductRepository(session=session).add_all(data=list_new_products)

    @classmethod
    async def check_aggregation_product(cls, session: AsyncSession, code_product: str, party_id: int) -> dict:
        """Проверка агрегации продукции"""
        existing_product: Optional[Product] = await cls._check_existing_product(session=session,
                                                                                code_product=code_product)

        if not existing_product:
            raise HTTPException(status_code=404, detail="not found product")

        if existing_product.party_id != party_id:
            raise HTTPException(status_code=400, detail="unique code is attached to another batch")

        existing_party: Optional[Party] = await PartyRepository(session=session).find_one(id_data=party_id)

        if existing_party.status_closed:
            raise HTTPException(status_code=400, detail="batch is closed")

        if existing_product.is_aggregated:
            raise HTTPException(status_code=400, detail=f"unique code already used at {existing_product.aggregated_at}")

        new_state_is_aggregated = {
            "is_aggregated": True,
            "aggregated_at": datetime.utcnow()
        }
        model_product: Product = await ProductRepository(session=session).update_one(id_data=existing_product.id,
                                                                                     new_data=new_state_is_aggregated)

        return {"code_product": model_product.code_product}

    @staticmethod
    async def _check_existing_product(session: AsyncSession, code_product: str) -> Optional[Product]:
        """Проверка уже существующей продукции"""
        return await ProductRepository(session=session).find_one_by_params(**{"code_product": code_product})


product_service: ProductService = ProductService()
