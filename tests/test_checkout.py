import pytest
from shopping_site.cart import add_item
from shopping_site.catalog import Catalog
from shopping_site.checkout import checkout
from shopping_site.models import Product, Cart


def test_checkout_computes_total():
    catalog = Catalog()
    catalog.add_product(Product(id="p1", name="Widget", price_cents=150))
    cart = Cart()
    add_item(cart, "p1", 2)
    order = checkout(cart, catalog)
    assert order.total_cents == 300


def test_checkout_missing_product_raises():
    catalog = Catalog()
    cart = Cart()
    add_item(cart, "missing", 1)
    with pytest.raises(KeyError):
        checkout(cart, catalog)
