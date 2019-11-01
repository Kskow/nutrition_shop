from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from shop.models.product import Product
from shop.permissions.is_staff_or_read_only import IsStaffOrReadOnly
from shop.serializers.product import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Returns information about specific Product

    list:
    Returns information about specifically filtered products

    create:
    Add new product if user is staff user

    update:
    Update product if user is staff user

    delete:
    Delete product if user is staff user
    """

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category", "company", "is_promoted", "is_in_stock"]
    permission_classes = (IsStaffOrReadOnly,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
