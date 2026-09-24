"""Encapsulation: a Customer with a private cart and balance."""

from __future__ import annotations

from typing import List

from models.product import Product
from models.payment import Paymentable


class Customer:
    """Represents a shopper with balance and a shopping cart.

    Internal state is kept private and only mutated through well-defined
    methods, demonstrating Encapsulation.
    """

    def __init__(self, name: str, balance: float) -> None:
        self._name = name
        self._balance = balance
        self._cart: List[Product] = []

    # --- Getters (Encapsulation) ---
    @property
    def name(self) -> str:
        return self._name

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def cart(self) -> List[Product]:
        return list(self._cart)

    # --- Cart behaviour ---
    def add_to_cart(self, product: Product, quantity: int = 1) -> None:
        """Add one or more units of a product to the cart.

        ``quantity`` is kept separate from the product's stock so the same
        method can be used for both the initial add and the ``+`` control in
        the customer screen.
        """
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if product.quantity < quantity:
            raise ValueError(
                f"Only {product.quantity} unit(s) of {product.name} available."
            )

        self._cart.extend([product] * quantity)
        product.quantity -= quantity

    def remove_from_cart(
        self, product_name: str, quantity: int | None = None
    ) -> int:
        """Remove units from the cart and return the number removed.

        Passing ``None`` keeps the original behaviour and removes every unit
        of the product. Passing a positive quantity removes at most that many
        units, which is useful for the ``-`` control in the UI. Removing a
        product that is not in the cart is a no-op and returns ``0``.
        """
        if quantity is not None and quantity < 1:
            raise ValueError("Quantity must be at least 1.")

        available = self.get_cart_quantity(product_name)
        if available == 0:
            return 0

        remove_count = (
            available if quantity is None else min(quantity, available)
        )
        remaining = remove_count
        updated_cart: List[Product] = []

        for product in self._cart:
            if product.name == product_name and remaining > 0:
                product.quantity += 1
                remaining -= 1
            else:
                updated_cart.append(product)

        self._cart = updated_cart
        return remove_count

    def get_cart_quantity(self, product_name: str) -> int:
        """Return how many units of a product are currently in the cart."""
        return sum(1 for product in self._cart if product.name == product_name)

    def get_total_price(self) -> float:
        return sum(p.calculate_price() for p in self._cart)

    def checkout(self, payment: Paymentable) -> str:
        """Settle the cart using any Paymentable implementation."""
        total = self.get_total_price()
        if self._balance < total:
            raise ValueError(f"{self._name} has insufficient balance.")
        self._balance -= total
        result = payment.pay(total)
        self._cart.clear()
        return f"{result} Remaining balance: {self._balance:.2f} baht."

    def __str__(self) -> str:
        return f"Customer(name={self._name!r}, balance={self._balance:.2f})"
