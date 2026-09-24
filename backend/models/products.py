"""Inheritance + Polymorphism: concrete product subclasses."""

from __future__ import annotations

from models.product import Product


class Electronics(Product):
    """Product with VAT (7%) added to the base price."""

    VAT_RATE = 0.07

    def __init__(self, name: str, price: float, quantity: int, brand: str = "") -> None:
        super().__init__(name, price, quantity)
        self._brand = brand

    @property
    def brand(self) -> str:
        return self._brand

    def calculate_price(self) -> float:
        return self._price * (1 + self.VAT_RATE)


class Clothing(Product):
    """Product with a seasonal discount (5%) applied."""

    DISCOUNT_RATE = 0.05

    def __init__(self, name: str, price: float, quantity: int, size: str = "M") -> None:
        super().__init__(name, price, quantity)
        self._size = size

    @property
    def size(self) -> str:
        return self._size

    def calculate_price(self) -> float:
        return self._price * (1 - self.DISCOUNT_RATE)


class Food(Product):
    """Perishable product sold at its base price."""

    def __init__(
        self, name: str, price: float, quantity: int, expiry_date: str = ""
    ) -> None:
        super().__init__(name, price, quantity)
        self._expiry_date = expiry_date

    @property
    def expiry_date(self) -> str:
        return self._expiry_date

    def calculate_price(self) -> float:
        return float(self._price)
