"""Domain model package for the Shop OOP system.

This package demonstrates the four pillars of OOP:
- Abstraction:     Product (abstract) & Paymentable (interface)
- Encapsulation:   private attributes with property accessors
- Inheritance:     Electronics / Clothing / Food extend Product
- Polymorphism:    calculate_price(), pay()/refund() behaviour
"""

from models.product import Product
from models.products import Electronics, Clothing, Food
from models.payment import (
    Paymentable,
    CashPayment,
    CreditCardPayment,
    PromptPayPayment,
)
from models.customer import Customer
from models.shop import Shop

__all__ = [
    "Product",
    "Electronics",
    "Clothing",
    "Food",
    "Paymentable",
    "CashPayment",
    "CreditCardPayment",
    "PromptPayPayment",
    "Customer",
    "Shop",
]
