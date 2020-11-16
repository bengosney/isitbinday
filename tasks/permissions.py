# Third Party
from django.core.exceptions import PermissionDenied
from rest_framework import permissions
from django_oso.auth import authorize

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object
    """

    def has_object_permission(self, request, view, obj):
        print(f'has_object_permission: {view.action}')
        try:
            authorize(request, obj, action=view.action)
        except PermissionDenied:
            return False

        return True