# Django
from django import forms
from django.contrib import admin

# Locals
from . import models


class householdAdminForm(forms.ModelForm):

    class Meta:
        model = models.household
        fields = "__all__"


class householdAdmin(admin.ModelAdmin):
    form = householdAdminForm
    list_display = [
        "created",
        "last_updated",
        "name",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]


class memberAdminForm(forms.ModelForm):

    class Meta:
        model = models.member
        fields = "__all__"


class memberAdmin(admin.ModelAdmin):
    form = memberAdminForm
    list_display = [
        "level",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]


admin.site.register(models.household, householdAdmin)
admin.site.register(models.member, memberAdmin)
