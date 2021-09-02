# Django
from django import forms

# Locals
from . import models


class ingredientForm(forms.ModelForm):
    class Meta:
        model = models.Ingredient
        fields = [
            "name",
            "quantity",
            "unit",
            "recipe",
        ]


class recipeForm(forms.ModelForm):
    class Meta:
        model = models.Recipe
        fields = [
            "name",
            "time",
            "description",
            "link",
        ]


class unitForm(forms.ModelForm):
    class Meta:
        model = models.Unit
        fields = [
            "name",
        ]


class stepForm(forms.ModelForm):
    class Meta:
        model = models.Step
        fields = [
            "description",
            "recipe",
        ]
