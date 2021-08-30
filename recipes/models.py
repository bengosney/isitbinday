# Django
from django.db import models
from django.urls import reverse

# Third Party
from django_oso.models import AuthorizedModel


class OwnedModel(AuthorizedModel):
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class ingredient(OwnedModel):

    # Relationships
    unit = models.ForeignKey("recipes.unit", related_name="ingredients", on_delete=models.CASCADE)
    recipe = models.ForeignKey("recipes.recipe", related_name="ingredients", on_delete=models.CASCADE)

    # Fields
    name = models.CharField(max_length=30)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("recipes_ingredient_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("recipes_ingredient_update", args=(self.pk,))


class recipe(OwnedModel):

    # Fields
    name = models.CharField(max_length=30)
    time = models.DurationField(default=0)
    description = models.TextField(max_length=512, default="", blank=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    link = models.URLField(max_length=200, default="", blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("recipes_recipe_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("recipes_recipe_update", args=(self.pk,))


class unit(OwnedModel):

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    name = models.CharField(max_length=30)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("recipes_unit_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("recipes_unit_update", args=(self.pk,))


class step(OwnedModel):

    # Relationships
    recipe = models.ForeignKey("recipes.recipe", related_name="steps", on_delete=models.CASCADE)

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    description = models.TextField(max_length=512)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("recipes_step_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("recipes_step_update", args=(self.pk,))
