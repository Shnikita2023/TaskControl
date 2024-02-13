from fastapi import APIRouter

from .parties.routers import router_party
from .products.routers import router_product

router = APIRouter()
router.include_router(router=router_party)
router.include_router(router=router_product)
