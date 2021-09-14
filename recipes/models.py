# Standard Library
from typing import Union

# Django
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

# Third Party
import pint
from django_extensions.db.fields import AutoSlugField
from django_oso.models import AuthorizedModel


class OwnedModel(AuthorizedModel):
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        abstract = True


class Ingredient(OwnedModel):

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

    @property
    def quantity_class(self) -> Union[pint.Quantity]:
        if self.unit.unit_class is None:
            raise pint.UndefinedUnitError

        return self.quantity * self.unit.unit_class

    @property
    def quantity_base_units(self):
        return self.quantity_class.to_base_units()

    @property
    def quantity_metric(self):
        try:
            return self.quantity_base_units.magnitude
        except pint.UndefinedUnitError:
            return self.quantity

    @property
    def quantity_metric_unit(self):
        try:
            return self.quantity_base_units.units
        except pint.UndefinedUnitError:
            return self.unit.name

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("recipes_ingredient_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("recipes_ingredient_update", args=(self.pk,))


class Recipe(OwnedModel):
    name = models.CharField(_("Name"), max_length=30)
    time = models.DurationField(_("Time to cook"), default=0)
    description = models.TextField(_("Description"), max_length=512, default="", blank=True)
    slug = AutoSlugField(_("Slug"), populate_from=("name",))
    link = models.URLField(_("Original URL"), max_length=200, default="", blank=True)
    last_updated = models.DateTimeField(_("Last Updated"), auto_now=True, editable=False)
    created = models.DateTimeField(_("Created"), auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("recipes_recipe_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("recipes_recipe_update", args=(self.pk,))


class Unit(OwnedModel):

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    name = models.CharField(max_length=30)

    _units = None

    @classmethod
    def _get_units(cls) -> pint.UnitRegistry:
        if cls._units is None:
            cls._units = pint.UnitRegistry(system="cooking")
            cls._units.load_definitions(
                """
@system cooking using international, Gaussian, ESU
    centimeter
    gram
    second
    millilitres
@end
            """.splitlines(),
                is_resource=False,
            )

        return cls._units

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    @property
    def unit_class(self) -> Union[pint.Quantity, None]:
        reg = self._get_units()
        try:
            cls = reg(f"{self.name}".replace(" ", "_").lower())
            if not isinstance(cls, pint.Quantity):
                raise pint.UndefinedUnitError()

            return cls
        except pint.UndefinedUnitError:
            return None

    def get_absolute_url(self):
        return reverse("recipes_unit_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("recipes_unit_update", args=(self.pk,))


class Step(OwnedModel):

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
