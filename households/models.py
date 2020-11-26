# Django
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


class household(models.Model):

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    name = models.CharField(max_length=30)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("households_household_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("households_household_update", args=(self.pk,))


class member(models.Model):

    LEVEL_VIEW = 10
    LEVEL_USER = 20
    LEVEL_ADMIN = 30

    LEVELS = [
        (LEVEL_VIEW, _('View only')),
        (LEVEL_USER, _('Member')),
        (LEVEL_ADMIN, _('Admin')),
    ]

    # Relationships
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    household = models.ForeignKey("households.household", on_delete=models.CASCADE)

    # Fields
    level = models.PositiveSmallIntegerField(default=0, choices=LEVELS)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("households_member_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("households_member_update", args=(self.pk,))
