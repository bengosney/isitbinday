from django.contrib import admin
from django import forms

from . import models


class UnitOfMeasureAdminForm(forms.ModelForm):

    class Meta:
        model = models.UnitOfMeasure
        fields = "__all__"


class UnitOfMeasureAdmin(admin.ModelAdmin):
    form = UnitOfMeasureAdminForm
    list_display = [
        "name",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]


class StockAdminForm(forms.ModelForm):

    class Meta:
        model = models.Stock
        fields = "__all__"


class StockAdmin(admin.ModelAdmin):
    form = StockAdminForm
    list_display = [
        "last_updated",
        "added",
        "quantity",
        "created",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]


class CategoryAdminForm(forms.ModelForm):

    class Meta:
        model = models.Category
        fields = "__all__"


class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = [
        "name",
        "last_updated",
        "created",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]


class ProductAdminForm(forms.ModelForm):

    class Meta:
        model = models.Product
        fields = "__all__"


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = [
        "name",
        "last_updated",
        "created",
        "code",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]


class BrandAdminForm(forms.ModelForm):

    class Meta:
        model = models.Brand
        fields = "__all__"


class BrandAdmin(admin.ModelAdmin):
    form = BrandAdminForm
    list_display = [
        "name",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]


class LocationAdminForm(forms.ModelForm):

    class Meta:
        model = models.Location
        fields = "__all__"


class LocationAdmin(admin.ModelAdmin):
    form = LocationAdminForm
    list_display = [
        "type",
        "name",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]


admin.site.register(models.UnitOfMeasure, UnitOfMeasureAdmin)
admin.site.register(models.Stock, StockAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Brand, BrandAdmin)
admin.site.register(models.Location, LocationAdmin)
