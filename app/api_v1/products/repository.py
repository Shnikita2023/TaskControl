from app.api_v1.products.models import Product
from app.api_v1.repositories.base_repository import SQLAlchemyRepository


class ProductRepository(SQLAlchemyRepository):
    model: Product = Product
