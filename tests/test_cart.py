import pytest
from shopping_site.cart import add_item, total_items
from shopping_site.models import Cart


def test_add_item_accumulates_quantity():
    cart = Cart()
    add_item(cart, "p1", 2)
    add_item(cart, "p1", 3)
    assert total_items(cart) == 5


def test_add_item_rejects_non_positive():
    cart = Cart()
    with pytest.raises(ValueError):
        add_item(cart, "p1", 0)
