import shop


def test_version():
    assert shop.__version__ == "0.1.0"


def test_models():
    product = shop.Product(id="p100", name="Widget", price=12.5)
    assert product.id == "p100"
    assert product.name == "Widget"
    assert product.price == 12.5

    item = shop.CartItem(product_id="p100", quantity=3)
    assert item.product_id == "p100"
    assert item.quantity == 3


def test_catalog():
    products = shop.list_products()
    assert products

    first = products[0]
    assert shop.get_product(first.id) == first


def test_cart_total():
    products = shop.list_products()
    first = products[0]

    cart = shop.Cart()
    cart.add(first.id, quantity=2)

    assert cart.total(shop.get_product) == first.price * 2
