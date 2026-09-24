"""Customer endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from models.customer import Customer
from schemas import CustomerIn
from store import customers

router = APIRouter(prefix="/api/customers", tags=["customers"])


def _to_dict(customer: Customer) -> dict:
    cart_items: list[dict] = []

    for product in customer.cart:
        existing = next(
            (item for item in cart_items if item["name"] == product.name),
            None,
        )
        if existing is None:
            cart_items.append(
                {
                    "name": product.name,
                    "price": round(product.calculate_price(), 2),
                    "category": product.__class__.__name__,
                    "quantity": 1,
                }
            )
        else:
            existing["quantity"] += 1

    return {
        "name": customer.name,
        "balance": round(customer.balance, 2),
        "cart_total": round(customer.get_total_price(), 2),
        "cart_items": cart_items,
    }


@router.post("")
def create_customer(item: CustomerIn) -> dict:
    if item.name in customers:
        raise HTTPException(status_code=400, detail="Customer already exists")
    customers[item.name] = Customer(item.name, item.balance)
    return {"message": f"Created customer {item.name}"}


@router.get("")
def list_customers() -> list[dict]:
    return [_to_dict(c) for c in customers.values()]