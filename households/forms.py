# Django
from django import forms

# Locals
from . import models


class householdForm(forms.ModelForm):
    class Meta:
        model = models.household
        fields = [
            "name",
        ]


class memberForm(forms.ModelForm):
    class Meta:
        model = models.member
        fields = [
            "level",
            "user",
            "household",
        ]
