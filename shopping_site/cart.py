from shopping_site.models import Cart, CartItem


def add_item(cart: Cart, product_id: str, quantity: int) -> None:
    if quantity <= 0:
        raise ValueError("quantity must be positive")
    for i, item in enumerate(cart.items):
        if item.product_id == product_id:
            cart.items[i] = CartItem(product_id=product_id, quantity=item.quantity + quantity)
            return
    cart.items.append(CartItem(product_id=product_id, quantity=quantity))


def total_items(cart: Cart) -> int:
    return sum(item.quantity for item in cart.items)
