# Django
from django.db import models

# Locals
from . import OwnerManager


class OwnedModel(models.Model):
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE, blank=True, null=True)

    objects = OwnerManager()

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class OwnedTimeStampedModel(OwnedModel, TimeStampedModel):
    class Meta:
        abstract = True
