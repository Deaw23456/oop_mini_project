"""REST routers for the Shop API."""

from api.routers.products import router as products_router
from api.routers.customers import router as customers_router
from api.routers.cart import router as cart_router

__all__ = ["products_router", "customers_router", "cart_router"]