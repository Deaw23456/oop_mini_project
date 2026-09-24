"""Abstraction + Encapsulation: the Product base class."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Product(ABC):
    """Abstract product with encapsulated (private) attributes.

    Subclasses must implement :meth:`calculate_price` — this is where
    Polymorphism is realised.
    """

    def __init__(self, name: str, price: float, quantity: int) -> None:
        self._name = name
        self._price = price
        self._quantity = quantity

    # --- Getters / Setters (Encapsulation) ---
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self._price = value

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        if value < 0:
            raise ValueError("Quantity cannot be negative.")
        self._quantity = value

    @abstractmethod
    def calculate_price(self) -> float:
        """Final selling price for one unit (overridden per subclass)."""

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(name={self._name!r}, "
            f"price={self._price}, qty={self._quantity})"
        )
