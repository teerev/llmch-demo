from __future__ import annotations

from collections.abc import Callable

from .models import CartItem, Product


class Cart:
    def __init__(self) -> None:
        self._quantities: dict[str, int] = {}

    def add(self, product_id: str, quantity: int = 1) -> None:
        self._quantities[product_id] = self._quantities.get(product_id, 0) + quantity

    def remove(self, product_id: str) -> None:
        self._quantities.pop(product_id, None)

    def items(self) -> list[CartItem]:
        return [
            CartItem(product_id=product_id, quantity=quantity)
            for product_id, quantity in self._quantities.items()
        ]

    def total(self, lookup: Callable[[str], Product | None]) -> float:
        total = 0.0
        for product_id, quantity in self._quantities.items():
            product = lookup(product_id)
            if product is None:
                continue
            total += product.price * quantity
        return total
