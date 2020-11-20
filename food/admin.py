from django.contrib import admin
from django import forms

from . import models


class categoryAdminForm(forms.ModelForm):

    class Meta:
        model = models.category
        fields = "__all__"


class categoryAdmin(admin.ModelAdmin):
    form = categoryAdminForm
    list_display = [
        "name",
        "last_updated",
        "created",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]


class productAdminForm(forms.ModelForm):

    class Meta:
        model = models.product
        fields = "__all__"


class productAdmin(admin.ModelAdmin):
    form = productAdminForm
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


class brandAdminForm(forms.ModelForm):

    class Meta:
        model = models.brand
        fields = "__all__"


class brandAdmin(admin.ModelAdmin):
    form = brandAdminForm
    list_display = [
        "name",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]


admin.site.register(models.category, categoryAdmin)
admin.site.register(models.product, productAdmin)
admin.site.register(models.brand, brandAdmin)
