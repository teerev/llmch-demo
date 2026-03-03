from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class Product:
    id: str
    name: str
    price_cents: int


@dataclass(frozen=True)
class CartItem:
    product_id: str
    quantity: int


@dataclass
class Cart:
    items: List[CartItem] = field(default_factory=list)


@dataclass(frozen=True)
class Order:
    items: List[CartItem]
    total_cents: int
