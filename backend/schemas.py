"""Pydantic request/validation schemas for the API."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

ProductCategory = Literal["electronics", "clothing", "food"]
PaymentMethod = Literal["cash", "card", "promptpay"]


class ProductIn(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)
    category: ProductCategory
    brand: Optional[str] = ""
    size: Optional[str] = "M"
    expiry_date: Optional[str] = ""


class CustomerIn(BaseModel):
    name: str = Field(min_length=1)
    balance: float = Field(ge=0)


class AddToCartIn(BaseModel):
    customer_name: str
    product_name: str
    quantity: int = Field(default=1, ge=1)


class RemoveFromCartIn(BaseModel):
    customer_name: str
    product_name: str
    # Omit quantity to preserve the original remove-all behaviour.
    quantity: Optional[int] = Field(default=None, ge=1)


class CheckoutIn(BaseModel):
    customer_name: str
    payment: PaymentMethod