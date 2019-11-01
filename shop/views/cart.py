from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import viewsets

from shop.models.cart import Cart
from shop.serializers.cart import CartSerializer


class CartViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Returns information about specific cart

    list:
    Returns information about specifically filtered cart

    create:
    Create new cart item

    update:
    Update cart

    delete:
    Delete cart
    """

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user"]
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
