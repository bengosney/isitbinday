# Django
from django import forms

# Locals
from . import models


class authorForm(forms.ModelForm):
    class Meta:
        model = models.Author
        fields = [
            "name",
        ]


class bookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = [
            "publish_date",
            "title",
            "isbn",
            "authors",
        ]
