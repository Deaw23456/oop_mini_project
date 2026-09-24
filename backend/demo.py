"""CLI demo: demonstrates all 4 OOP principles."""

from models.product import Product
from models.products import Electronics, Clothing, Food
from models.payment import CashPayment, CreditCardPayment, PromptPayPayment
from models.customer import Customer
from models.shop import Shop


def demonstrate_abstraction_and_polymorphism() -> list[Product]:
    print("=" * 60)
    print("1) ABSTRACTION + POLYMORPHISM (calculate_price differs per type)")
    print("=" * 60)

    products: list[Product] = [
        Electronics("iPhone", 30000, 5, brand="Apple"),
        Clothing("T-Shirt", 500, 20, size="L"),
        Food("Milk", 50, 30, expiry_date="2026-12-31"),
    ]

    for p in products:
        print(f"  {p.name:<12} -> {p.calculate_price():.2f} baht")
    return products


def demonstrate_encapsulation() -> Customer:
    print()
    print("=" * 60)
    print("2) ENCAPSULATION (private fields + property access)")
    print("=" * 60)

    cust = Customer("Somchai", 50000)
    print(f"  Created: {cust}")
    print("  Balance is read-only -> accessed via getter:")
    print(f"    cust.balance = {cust.balance:.2f} baht")
    print("  Balance can only change through checkout():")
    print(f"    -> checkout() reduces it when paying for a cart")
    return cust


def demonstrate_inheritance(products: list[Product]) -> None:
    print()
    print("=" * 60)
    print("3) INHERITANCE + is-a relationships")
    print("=" * 60)
    for p in products:
        print(
            f"  {p.name} is instance of Product? "
            f"{isinstance(p, Product)} (class: {p.__class__.__name__})"
        )


def demonstrate_payment_polymorphism(cust: Customer) -> None:
    print()
    print("=" * 60)
    print("4) POLYMORPHISM via interface (Paymentable)")
    print("=" * 60)
    print(f"  {cust.name} cart total: {cust.get_total_price():.2f} baht")
    for payment in (CashPayment(), CreditCardPayment(), PromptPayPayment()):
        print(f"  -> {type(payment).__name__}: {payment.pay(cust.get_total_price())}")


def main() -> None:
    products = demonstrate_abstraction_and_polymorphism()

    shop = Shop("My Little Shop")
    for p in products:
        shop.add_product(p)

    cust = demonstrate_encapsulation()
    demonstrate_inheritance(products)

    cust.add_to_cart(products[0])  # iPhone
    cust.add_to_cart(products[1])  # T-Shirt
    demonstrate_payment_polymorphism(cust)

    print()
    print("  Doing checkout with CashPayment...")
    print(f"  {cust.checkout(CashPayment())}")

    print()
    print("=" * 60)
    print("5) SHOP MANAGING INVENTORY")
    print("=" * 60)
    shop.list_products()
    print(f"  {shop}")


if __name__ == "__main__":
    main()