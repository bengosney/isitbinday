# Django
from django import forms
from django.contrib import admin

# Locals
from . import models


class tagAdminForm(forms.ModelForm):
    class Meta:
        model = models.Tag
        fields = "__all__"


class tagAdmin(admin.ModelAdmin):
    form = tagAdminForm
    list_display = [
        "title",
        "last_updated",
        "created",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]


admin.site.register(models.Tag, tagAdmin)
