from fastapi import APIRouter

router_product = APIRouter(
    prefix="/products",
    tags=["Products"]
)
