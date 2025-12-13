# Third Party
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Custom permission to only allow owners of an object."""

    def has_object_permission(self, request, view, obj):
        print(f"has_object_permission: {view.action}")
        return request.user == obj.owner
