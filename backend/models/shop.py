"""Encapsulation: a Shop that manages a private product inventory."""

from __future__ import annotations

from typing import List, Optional

from models.product import Product


class Shop:
    """Owns the product inventory and controls access to it."""

    def __init__(self, name: str) -> None:
        self._name = name
        self._inventory: List[Product] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def inventory(self) -> List[Product]:
        return list(self._inventory)

    def add_product(self, product: Product) -> None:
        self._inventory.append(product)

    def remove_product(self, product_name: str) -> None:
        self._inventory = [p for p in self._inventory if p.name != product_name]

    def find_product(self, product_name: str) -> Optional[Product]:
        return next((p for p in self._inventory if p.name == product_name), None)

    def list_products(self) -> None:
        if not self._inventory:
            print("  (inventory is empty)")
            return
        for p in self._inventory:
            print(f"  - {p.name}: {p.calculate_price():.2f} baht (qty {p.quantity})")

    def __str__(self) -> str:
        return f"Shop(name={self._name!r}, products={len(self._inventory)})"
