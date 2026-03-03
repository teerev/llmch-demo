from typing import Dict, List, Optional
from shopping_site.models import Product


class Catalog:
    def __init__(self) -> None:
        self._products: Dict[str, Product] = {}

    def add_product(self, product: Product) -> None:
        self._products[product.id] = product

    def list_products(self) -> List[Product]:
        return list(self._products.values())

    def get_product(self, product_id: str) -> Optional[Product]:
        return self._products.get(product_id)
