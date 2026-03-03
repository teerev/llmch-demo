from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    id: str
    name: str
    price: float


@dataclass(frozen=True)
class CartItem:
    product_id: str
    quantity: int
