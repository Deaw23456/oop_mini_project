"""Shared application state (singletons for shop and customers)."""

from __future__ import annotations

from typing import Dict

from models.customer import Customer
from models.products import Electronics, Clothing, Food
from models.shop import Shop

# The one and only shop instance shared by all routes.
shop = Shop("My Little Shop")

# In-memory customer registry keyed by name.
customers: Dict[str, Customer] = {}


def seed_data() -> None:
    """Populate the shop with a few example products."""
    shop.add_product(Electronics("iPhone", 30000, 5, brand="Apple"))
    shop.add_product(Clothing("T-Shirt", 500, 20, size="L"))
    shop.add_product(Food("Milk", 50, 30, expiry_date="2026-12-31"))