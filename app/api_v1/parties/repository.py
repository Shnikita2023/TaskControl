from app.api_v1.parties.models import Party
from app.api_v1.repositories.base_repository import SQLAlchemyRepository


class PartyRepository(SQLAlchemyRepository):
    model: Party = Party
