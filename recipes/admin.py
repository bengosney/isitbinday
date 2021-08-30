# Django
from django import forms
from django.contrib import admin

# Locals
from . import models


class ingredientInline(admin.TabularInline):
    model = models.ingredient


class stepInline(admin.TabularInline):
    model = models.step


class ingredientAdminForm(forms.ModelForm):
    class Meta:
        model = models.ingredient
        fields = "__all__"


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
        model = models.recipe
        fields = "__all__"


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
        model = models.unit
        fields = "__all__"


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
        model = models.step
        fields = "__all__"


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


admin.site.register(models.ingredient, ingredientAdmin)
admin.site.register(models.recipe, recipeAdmin)
admin.site.register(models.unit, unitAdmin)
admin.site.register(models.step, stepAdmin)
