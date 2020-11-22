# Django
from django import forms
from django.db.models import fields

# Locals
from . import models


class UnitOfMeasureForm(forms.ModelForm):
    class Meta:
        model = models.UnitOfMeasure
        fields = [
            "name",
        ]


class StockForm(forms.ModelForm):
    class Meta:
        model = models.Stock
        fields = [
            "quantity",
            "location",
            "unit_of_measure",
            "product",
        ]


class TransferForm(forms.ModelForm):
    class Meta:
        model = models.Transfer
        fields = [
            "origin",
            "destination",
        ]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = [
            "name",
        ]


class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = [
            "name",
            "code",
            "categories",
            "brand",
        ]


class BrandForm(forms.ModelForm):
    class Meta:
        model = models.Brand
        fields = [
            "name",
        ]


class LocationForm(forms.ModelForm):
    class Meta:
        model = models.Location
        fields = [
            "temperature",
            "name",
        ]
