from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Permission which allows staff user to create/edit/delete object.
    Allows normal users to fetch.
    """

    message = "You are not allowed to perform this action!"

    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff
