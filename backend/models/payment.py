"""Abstraction + Polymorphism: the payment contract and its implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Paymentable(ABC):
    """Contract every payment method must satisfy."""

    @abstractmethod
    def pay(self, amount: float) -> str:
        """Process a payment and return a human-readable receipt."""

    @abstractmethod
    def refund(self, amount: float) -> str:
        """Process a refund and return a human-readable receipt."""


class CashPayment(Paymentable):
    """Payment settled in cash — no extra fee."""

    def pay(self, amount: float) -> str:
        return f"Paid {amount:.2f} baht in cash."

    def refund(self, amount: float) -> str:
        return f"Refunded {amount:.2f} baht in cash."


class CreditCardPayment(Paymentable):
    """Payment via credit card with an additional service fee."""

    FEE_RATE = 0.03

    def pay(self, amount: float) -> str:
        total = amount * (1 + self.FEE_RATE)
        return (
            f"Paid {amount:.2f} baht by credit card "
            f"(total {total:.2f} with 3% fee)."
        )

    def refund(self, amount: float) -> str:
        return f"Refunded {amount:.2f} baht to credit card."


class PromptPayPayment(Paymentable):
    """Payment via PromptPay — no extra fee."""

    def pay(self, amount: float) -> str:
        return f"Paid {amount:.2f} baht via PromptPay."

    def refund(self, amount: float) -> str:
        return f"Refunded {amount:.2f} baht via PromptPay."
