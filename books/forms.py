# Django
from django import forms

# Locals
from . import models


class AuthorForm(forms.ModelForm):
    class Meta:
        model = models.Author
        fields = [
            "name",
        ]


class BbookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = [
            "publish_date",
            "title",
            "isbn",
            "authors",
        ]
