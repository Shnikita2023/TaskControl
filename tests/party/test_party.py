from httpx import Response, AsyncClient

from tests.test_data import parties, parties_answer, updated_parties, updated_parties_filter


class TestParty:
    """Класс для тестирования партии"""

    async def test_create_party(self, async_client: AsyncClient) -> None:
        response_party: Response = await async_client.post(url="/api/v1/parties/", json=parties)
        assert response_party.status_code == 201
        assert response_party.json() == {"message": "the request was completed successfully"}

    async def test_get_party(self, async_client: AsyncClient) -> None:
        response_party: Response = await async_client.get(url="/api/v1/parties/1")
        assert response_party.status_code == 200
        assert len(response_party.json()) == 15
        assert response_party.json() == parties_answer

    async def test_update_party(self, async_client: AsyncClient) -> None:
        response_party: Response = await async_client.patch(url="/api/v1/parties/1",
                                                            json=updated_parties)
        assert response_party.status_code == 200
        assert len(response_party.json()) == 12
        assert response_party.json() == updated_parties

    async def test_get_party_by_filter(self, async_client: AsyncClient) -> None:
        response_party: Response = await async_client.get(url="/api/v1/parties/?value_party=22222&"
                                                              "offset=0&limit=1&name_party=party_number")
        assert response_party.status_code == 200
        assert len(response_party.json()) == 1
        assert response_party.json()[0] == updated_parties_filter
