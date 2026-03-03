from shopping_site.catalog import Catalog
from shopping_site.models import Product


def test_catalog_add_and_get():
    catalog = Catalog()
    catalog.add_product(Product(id="p1", name="Widget", price_cents=150))
    assert catalog.get_product("p1").name == "Widget"


def test_catalog_list_products():
    catalog = Catalog()
    catalog.add_product(Product(id="p1", name="Widget", price_cents=150))
    catalog.add_product(Product(id="p2", name="Gadget", price_cents=250))
    products = catalog.list_products()
    assert len(products) == 2
