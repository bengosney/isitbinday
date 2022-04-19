# Standard Library
from datetime import timedelta

# Django
from django.db import models

# Third Party
from taggit.managers import TaggableManager


class Exercise(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    tags = TaggableManager(blank=True)
    difficulty = models.PositiveSmallIntegerField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Workout(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    exercises = models.ManyToManyField(Exercise, blank=True)
    tags = TaggableManager(blank=True)

    round_count = models.IntegerField(default=20)
    round_length = models.DurationField(default=timedelta(seconds=45))
    interval = models.DurationField(default=timedelta(seconds=15))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
