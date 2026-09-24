"""Product endpoints."""

from __future__ import annotations

from typing import Dict, Type

from fastapi import APIRouter, HTTPException

from models.product import Product
from models.products import Electronics, Clothing, Food
from schemas import ProductIn
from store import shop

router = APIRouter(prefix="/api/products", tags=["products"])

# Registry mapping a category name to its product class.
_PRODUCT_TYPES: Dict[str, Type[Product]] = {
    "electronics": Electronics,
    "clothing": Clothing,
    "food": Food,
}


def _to_dict(product: Product) -> dict:
    return {
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity,
        "category": product.__class__.__name__,
        "calculated_price": round(product.calculate_price(), 2),
    }


def _build_product(item: ProductIn) -> Product:
    """Instantiate the right subclass with its extra attributes."""
    product_type = _PRODUCT_TYPES[item.category]

    if product_type is Electronics:
        return Electronics(item.name, item.price, item.quantity, brand=item.brand)
    if product_type is Clothing:
        return Clothing(item.name, item.price, item.quantity, size=item.size)
    return Food(item.name, item.price, item.quantity, expiry_date=item.expiry_date)


@router.get("")
def list_products() -> list[dict]:
    return [_to_dict(p) for p in shop.inventory]


@router.post("")
def add_product(item: ProductIn) -> dict:
    product = _build_product(item)
    shop.add_product(product)
    return {"message": f"Added {item.name}"}


@router.delete("/{name}")
def remove_product(name: str) -> dict:
    shop.remove_product(name)
    return {"message": f"Removed {name}"}