from django.core.validators import MinValueValidator
from django.db import models

from shop.models.product import Product
from shop.models.cart import Cart


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, blank=False)
    quantity = models.IntegerField(default=1, blank=False, validators=[MinValueValidator(1)])
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return f", {self.cart.pk}, {self.product}, {self.quantity}"
