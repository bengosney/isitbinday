# Django
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class AuthDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="authdetails")
    homeGroups = models.ManyToManyField("HomeGroup", related_name="usergroup")

    def __str__(self) -> str:
        return f"{self.__class__.__name__} for {self.user}"


class HomeGroup(models.Model):
    name = models.CharField(max_length=50)


@receiver(post_save, sender=User)
def create_user_details(sender, instance, created: bool, **kwargs) -> None:
    if created:
        AuthDetails.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_details(sender, instance, **kwargs) -> None:
    try:
        instance.authdetails.save()
    except AuthDetails.DoesNotExist:
        AuthDetails.objects.create(user=instance)
