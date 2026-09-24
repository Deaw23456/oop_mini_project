"""Shopping cart endpoints."""

from __future__ import annotations

from typing import Dict

from fastapi import APIRouter, HTTPException

from models.customer import Customer
from models.payment import Paymentable, CashPayment, CreditCardPayment, PromptPayPayment
from schemas import AddToCartIn, CheckoutIn, RemoveFromCartIn
from store import shop, customers

router = APIRouter(prefix="/api/cart", tags=["cart"])

PAYMENTS: Dict[str, Paymentable] = {
    "cash": CashPayment(),
    "card": CreditCardPayment(),
    "promptpay": PromptPayPayment(),
}


def _get_customer(name: str) -> Customer:
    customer = customers.get(name)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.post("/add")
def add_item(item: AddToCartIn) -> dict:
    customer = _get_customer(item.customer_name)
    product = shop.find_product(item.product_name)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    try:
        customer.add_to_cart(product, item.quantity)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "message": (
            f"Added {item.quantity} unit(s) of {item.product_name} "
            f"to {item.customer_name}'s cart"
        )
    }


@router.post("/remove")
def remove_item(item: RemoveFromCartIn) -> dict:
    customer = _get_customer(item.customer_name)

    try:
        removed = customer.remove_from_cart(item.product_name, item.quantity)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "message": (
            f"Removed {removed} unit(s) of {item.product_name} "
            f"from {item.customer_name}'s cart"
        )
    }


@router.post("/checkout")
def checkout(item: CheckoutIn) -> dict:
    customer = _get_customer(item.customer_name)
    payment = PAYMENTS.get(item.payment)
    if payment is None:
        raise HTTPException(status_code=400, detail="Unknown payment method")
    try:
        result = customer.checkout(payment)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"message": result}