# Django
from django import forms

# Locals
from . import models


class ingredientForm(forms.ModelForm):
    class Meta:
        model = models.ingredient
        fields = [
            "name",
            "quantity",
            "unit",
            "recipe",
        ]


class recipeForm(forms.ModelForm):
    class Meta:
        model = models.recipe
        fields = [
            "name",
            "time",
            "description",
            "link",
        ]


class unitForm(forms.ModelForm):
    class Meta:
        model = models.unit
        fields = [
            "name",
        ]


class stepForm(forms.ModelForm):
    class Meta:
        model = models.step
        fields = [
            "description",
            "recipe",
        ]
