# Third Party
# Django
from django.core.exceptions import PermissionDenied

# Third Party
from django_oso.auth import authorize
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Custom permission to only allow owners of an object."""

    def has_object_permission(self, request, view, obj):
        try:
            authorize(request, obj, action=view.action)
        except PermissionDenied:
            return False

        return True
