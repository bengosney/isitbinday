# Django
from django import forms
from django.contrib import admin

# Locals
from . import models


class AuthorAdminForm(forms.ModelForm):
    class Meta:
        model = models.Author
        fields = ["name"]


class AuthorAdmin(admin.ModelAdmin):
    form = AuthorAdminForm
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


@admin.action(description="Mark as requiring data refetch")
def requires_refetch(modeladmin, request, queryset):
    queryset.update(requires_refetch=True)


class BookAdminForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = ["authors", "publish_date", "title", "isbn", "cover", "requires_refetch"]


class BookAdmin(admin.ModelAdmin):
    form = BookAdminForm
    list_display = [
        "title",
        "publish_date",
        "isbn",
        "requires_refetch",
    ]
    readonly_fields = [
        "created",
        "last_updated",
        "isbn",
    ]
    search_fields = [
        "title",
    ]
    actions = [requires_refetch]


class FailedAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Book, BookAdmin)
admin.site.register(models.FailedScan, FailedAdmin)
