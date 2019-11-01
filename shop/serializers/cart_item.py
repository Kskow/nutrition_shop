import decimal
from typing import Optional

from rest_framework import serializers

from shop.models.cart import Cart
from shop.models.cart_item import CartItem
from shop.models.product import Product
from shop.utils.cart import get_active_cart_or_create
from shop.utils.product import change_product_quantity_in_stock_depends_on_availability


class CartItemSerializer(serializers.ModelSerializer):

    price = serializers.SerializerMethodField()
    cart = serializers.SerializerMethodField()
    product = serializers.SlugRelatedField(slug_field="name", queryset=Product.objects.all())

    def get_price(self, obj) -> decimal.Decimal:
        return decimal.Decimal(f"{obj.product.normal_price}") * decimal.Decimal(f"{obj.quantity}")

    def get_cart(self, obj) -> Optional[Cart]:

        if "cart" not in self.context["request"].data:
            user = self.context["request"].user
            return get_active_cart_or_create(user).pk

    class Meta:
        model = CartItem
        fields = ("cart", "product", "quantity", "price")

    def create(self, validated_data) -> CartItem:
        change_product_quantity_in_stock_depends_on_availability(
            validated_data["product"], 0, validated_data["quantity"]
        )

        return CartItem.objects.create(**validated_data)

    def update(self, instance, validated_data) -> CartItem:
        instance.cart = validated_data.get("cart", instance.cart)
        instance.product = validated_data.get("product", instance.product)
        change_product_quantity_in_stock_depends_on_availability(
            instance.product, instance.quantity, validated_data["quantity"]
        )
        instance.quantity = validated_data.get("quantity", instance.quantity)
        instance.save()
        instance.product.save()
        return instance
