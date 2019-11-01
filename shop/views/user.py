from django.contrib.auth.models import User
from rest_framework import viewsets

from shop.permissions.is_staff_or_read_only import IsStaffOrReadOnly
from shop.serializers.user import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Returns information about specific User

    list:
    Returns information about all users
    """

    permission_classes = (IsStaffOrReadOnly,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
