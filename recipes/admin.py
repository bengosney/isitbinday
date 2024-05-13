# Django
from django import forms
from django.contrib import admin

# Locals
from . import models


class IngredientInline(admin.TabularInline):
    model = models.Ingredient


class StepInline(admin.TabularInline):
    model = models.Step


class IngredientAdminForm(forms.ModelForm):
    class Meta:
        model = models.Ingredient
        fields = [
            "name",
            "unit",
            "quantity",
        ]


class IngredientAdmin(admin.ModelAdmin):
    form = IngredientAdminForm
    list_display = [
        "name",
        "last_updated",
        "created",
        "quantity",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]


class RecipeAdminForm(forms.ModelForm):
    class Meta:
        model = models.Recipe
        fields = [
            "name",
            "time",
            "description",
        ]


class RecipeAdmin(admin.ModelAdmin):
    form = RecipeAdminForm
    list_display = [
        "name",
        "time",
        "description",
        "last_updated",
        "link",
        "created",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]

    inlines = [
        IngredientInline,
        StepInline,
    ]


class UnitAdminForm(forms.ModelForm):
    class Meta:
        model = models.Unit
        fields = [
            "name",
        ]


class UnitAdmin(admin.ModelAdmin):
    form = UnitAdminForm
    list_display = [
        "created",
        "last_updated",
        "name",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]


class StepAdminForm(forms.ModelForm):
    class Meta:
        model = models.Step
        fields = ["description"]


class StepAdmin(admin.ModelAdmin):
    form = StepAdminForm
    list_display = [
        "created",
        "last_updated",
        "description",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]


admin.site.register(models.Ingredient, IngredientAdmin)
admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.Unit, UnitAdmin)
admin.site.register(models.Step, StepAdmin)
