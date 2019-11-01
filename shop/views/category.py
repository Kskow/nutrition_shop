from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from shop.models.category import Category
from shop.permissions.is_staff_or_read_only import IsStaffOrReadOnly
from shop.serializers.category import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Returns information about specific category

    list:
    Returns information about specifically filtered categories

    create:
    Create new category if user is staff user

    update:
    Update category if user is staff user

    delete:
    Delete category if user is staff user
    """

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]
    permission_classes = (IsStaffOrReadOnly,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
