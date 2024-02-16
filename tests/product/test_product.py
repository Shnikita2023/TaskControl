import pytest
from httpx import AsyncClient, Response

from tests.test_data import products


class TestProduct:
    """Класс для тестирования продукции"""

    async def test_create_products(self, async_client: AsyncClient, create_party: int) -> None:
        """Создание продукции"""
        response_party: Response = await async_client.post(url="/api/v1/products/", json=products)
        assert response_party.status_code == 201
        assert response_party.json() == {"message": "the request was completed successfully"}

    @pytest.mark.parametrize(
        "code_product, party_id, status_code, error",
        [
            ("12gRV60MMsn1", 1, 400, "unique code already used at aggregated_at"),
            ("12gRV60MMsn3", 1, 400, "unique code is attached to another batch"),
            ("12gRV60MMsn4", 3, 400, "batch is closed"),
            ("12gRV60MMsn2", 1, 404, "not found product"),
        ]
    )
    async def test_aggregation_products(self,
                                        async_client: AsyncClient,
                                        code_product: str,
                                        party_id: int,
                                        status_code: int,
                                        error: str) -> None:
        """Проверка агрегации продукции к партии"""
        response_party: Response = await async_client.get(url=f"/api/v1/products/?code_product={code_product}&"
                                                              f"party_id={party_id}")

        assert response_party.status_code == status_code
        assert response_party.json()["detail"] == error
