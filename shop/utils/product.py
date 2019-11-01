from rest_framework import serializers

from shop.models.product import Product


def change_product_quantity_in_stock_depends_on_availability(
    product: Product, cart_actual_quantity: int, cart_quantity_to_change: int
) -> Product:
    if not product.is_in_stock:
        raise serializers.ValidationError("Product is not available now!")

    if product.quantity_in_stock - cart_quantity_to_change < 0:
        raise serializers.ValidationError(f"You can order only {product.quantity_in_stock}")

    product.quantity_in_stock += cart_actual_quantity - cart_quantity_to_change

    if product.quantity_in_stock == 0:
        product.is_in_stock = False

    return product.save()
