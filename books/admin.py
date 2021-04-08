# Django
from django import forms
from django.contrib import admin

# Locals
from . import models


class authorAdminForm(forms.ModelForm):
    class Meta:
        model = models.Author
        fields = "__all__"


class authorAdmin(admin.ModelAdmin):
    form = authorAdminForm
    list_display = [
        "name",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "name",
        "created",
        "last_updated",
    ]


class bookAdminForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = "__all__"


class bookAdmin(admin.ModelAdmin):
    form = bookAdminForm
    list_display = [
        "publish_date",
        "created",
        "title",
        "last_updated",
        "isbn",
    ]
    readonly_fields = [
        "publish_date",
        "created",
        "title",
        "last_updated",
        "isbn",
    ]


admin.site.register(models.Author, authorAdmin)
admin.site.register(models.Book, bookAdmin)