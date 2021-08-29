# Django
from django.db import models
from django.urls import reverse


class ingredient(models.Model):

    # Relationships
    unit = models.ForeignKey("recipes.unit", on_delete=models.CASCADE)
    recipe = models.ForeignKey("recipes.recipe", on_delete=models.CASCADE)

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


class recipe(models.Model):

    # Fields
    name = models.CharField(max_length=30)
    time = models.DurationField()
    description = models.TextField(max_length=512)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    link = models.URLField(max_length=200)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("recipes_recipe_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("recipes_recipe_update", args=(self.pk,))


class unit(models.Model):

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


class step(models.Model):

    # Relationships
    recipe = models.ForeignKey("recipes.recipe", on_delete=models.CASCADE)

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
