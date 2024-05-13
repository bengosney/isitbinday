# Django
from django import forms

# Locals
from . import models


class IngredientForm(forms.ModelForm):
    class Meta:
        model = models.Ingredient
        fields = [
            "name",
            "quantity",
            "unit",
            "recipe",
        ]


class RecipeForm(forms.ModelForm):
    class Meta:
        model = models.Recipe
        fields = [
            "name",
            "time",
            "description",
            "link",
        ]


class UnitForm(forms.ModelForm):
    class Meta:
        model = models.Unit
        fields = [
            "name",
        ]


class StepForm(forms.ModelForm):
    class Meta:
        model = models.Step
        fields = [
            "description",
            "recipe",
        ]
