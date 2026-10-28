# Django
from django.db import models


class OwnerManager(models.Manager):
    def for_user(self, user):
        """Return a queryset filtered by the owner."""
        if not getattr(user, "is_authenticated", False):
            return self.none()
        return self.filter(owner=user)
