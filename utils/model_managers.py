# Django
from django.db import models


class OwnerManager(models.Manager):
    def for_user(self, user):
        """Return a queryset filtered by the owner."""
        return self.filter(owner=user)
