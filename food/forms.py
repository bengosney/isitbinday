from django import forms
from . import models


class categoryForm(forms.ModelForm):
    class Meta:
        model = models.category
        fields = [
            "name",
        ]


class productForm(forms.ModelForm):
    class Meta:
        model = models.product
        fields = [
            "name",
            "code",
            "categories",
            "brand",
        ]


class brandForm(forms.ModelForm):
    class Meta:
        model = models.brand
        fields = [
            "name",
        ]
