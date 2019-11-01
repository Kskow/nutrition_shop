from django_filters.rest_framework.backends import DjangoFilterBackend
from shop.models.cart_item import CartItem
from shop.serializers.cart_item import CartItemSerializer
from rest_framework import viewsets


class CartItemViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Returns information about specific cart item

    list:
    Returns information about specifically filtered cart items

    create:
    Create new cart item

    update:
    Update cart item

    delete:
    Delete cart item
    """

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["product"]
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
