# Django
from django import forms
from django.contrib import admin

# Locals
from . import models


class ingredientInline(admin.TabularInline):
    model = models.Ingredient


class stepInline(admin.TabularInline):
    model = models.Step


class ingredientAdminForm(forms.ModelForm):
    class Meta:
        model = models.Ingredient
        fields = [
            "name",
            "unit",
            "quantity",
        ]


class ingredientAdmin(admin.ModelAdmin):
    form = ingredientAdminForm
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


class recipeAdminForm(forms.ModelForm):
    class Meta:
        model = models.Recipe
        fields = [
            "name",
            "time",
            "description",
        ]


class recipeAdmin(admin.ModelAdmin):
    form = recipeAdminForm
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
        ingredientInline,
        stepInline,
    ]


class unitAdminForm(forms.ModelForm):
    class Meta:
        model = models.Unit
        fields = [
            "name",
        ]


class unitAdmin(admin.ModelAdmin):
    form = unitAdminForm
    list_display = [
        "created",
        "last_updated",
        "name",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]


class stepAdminForm(forms.ModelForm):
    class Meta:
        model = models.Step
        fields = ["description"]


class stepAdmin(admin.ModelAdmin):
    form = stepAdminForm
    list_display = [
        "created",
        "last_updated",
        "description",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]


admin.site.register(models.Ingredient, ingredientAdmin)
admin.site.register(models.Recipe, recipeAdmin)
admin.site.register(models.Unit, unitAdmin)
admin.site.register(models.Step, stepAdmin)
