from django.contrib.auth.models import User

from shop.models.cart import Cart


def get_active_cart_or_create(user: User) -> Cart:
    if not has_user_active_cart(user):
        return Cart.objects.create(user=user, is_active=True)
    return Cart.objects.filter(user=user, is_active=True).first()


def has_user_active_cart(user: User) -> bool:
    carts = Cart.objects.filter(user=user)
    if carts is not None:
        for cart in carts:
            if cart.is_active:
                return True
    return False
