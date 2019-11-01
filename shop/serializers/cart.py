import decimal
from shop.models.cart_item import CartItem
from shop.models.cart import Cart
from rest_framework import serializers


class CartSerializer(serializers.ModelSerializer):
    cart_items = serializers.StringRelatedField(many=True)
    total_quantity = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    def get_total_quantity(self, obj) -> int:
        cart_items = CartItem.objects.filter(cart=obj.pk)
        return sum([item.quantity for item in cart_items])

    def get_total_price(self, obj) -> decimal.Decimal:
        cart_items = CartItem.objects.filter(cart=obj.pk)
        return sum([decimal.Decimal(item.quantity) * decimal.Decimal(item.product.normal_price) for item in cart_items])

    class Meta:
        model = Cart
        fields = ("user", "created_date", "last_update", "is_active", "cart_items", "total_quantity", "total_price")
        read_only_fields = ["created_date", "last_update"]
        validators = []
