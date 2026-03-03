from shopping_site.catalog import Catalog
from shopping_site.models import Cart, Order


def checkout(cart: Cart, catalog: Catalog) -> Order:
    total = 0
    for item in cart.items:
        product = catalog.get_product(item.product_id)
        if product is None:
            raise KeyError(item.product_id)
        total += product.price_cents * item.quantity
    return Order(items=list(cart.items), total_cents=total)
