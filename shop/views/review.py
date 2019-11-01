from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from shop.models.review import Review
from shop.permissions.is_owner_or_staff_or_read_only import IsOwnerOrStaffOrReadOnly
from shop.serializers.review import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Returns information about specific review

    list:
    Returns information about specifically filtered reviews

    create:
    Add new review

    update:
    Update review if belongs to user or if you are staff user

    delete:
    Delete review if user is owner or staff user
    """

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user", "rate", "product"]
    permission_classes = (IsOwnerOrStaffOrReadOnly,)
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)

    def perform_update(self, serializer) -> None:
        serializer.save(user=self.request.user)
