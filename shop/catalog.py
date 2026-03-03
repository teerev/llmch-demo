from __future__ import annotations

from .models import Product

# Fixed in-memory catalog
CATALOG: list[Product] = [
    Product(id="p1", name="Product 1", price=9.99),
    Product(id="p2", name="Product 2", price=19.99),
]


def list_products() -> list[Product]:
    """Return a new list copy of the in-memory catalog."""
    return list(CATALOG)


def get_product(product_id: str) -> Product | None:
    """Return the product matching product_id, or None if not found."""
    for product in CATALOG:
        if product.id == product_id:
            return product
    return None
