# Django
from django.db import models


class Tag(models.Model):
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    title = models.SlugField(max_length=30)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self) -> str:
        return str(self.title)

    @classmethod
    def getTag(cls, tag):
        try:
            return cls.objects.get(title=tag)
        except cls.DoesNotExist:
            return cls(title=tag)
