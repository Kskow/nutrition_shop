from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from shop.models.company import Company
from shop.permissions.is_staff_or_read_only import IsStaffOrReadOnly
from shop.serializers.company import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Returns information about specific Company

    list:
    Returns information about specifically filtered companies

    create:
    Create new company if user is staff user

    update:
    Update company if user is staff user

    delete:
    Delete company if user is staff user

    """

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]
    permission_classes = (IsStaffOrReadOnly,)
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
