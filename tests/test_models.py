from shopping_site.models import Product, Cart, CartItem, Order


def test_cart_default_items_empty():
    cart = Cart()
    assert cart.items == []


def test_product_fields():
    product = Product(id="p1", name="Widget", price_cents=150)
    assert product.price_cents == 150


def test_order_fields():
    item = CartItem(product_id="p1", quantity=2)
    order = Order(items=[item], total_cents=300)
    assert order.total_cents == 300
