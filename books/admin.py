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


@admin.action(description="Mark as requiring data refetch")
def requires_refetch(modeladmin, request, queryset):
    queryset.update(requires_refetch=True)


class bookAdminForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = "__all__"


class bookAdmin(admin.ModelAdmin):
    form = bookAdminForm
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


class failedAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Author, authorAdmin)
admin.site.register(models.Book, bookAdmin)
admin.site.register(models.FailedScan, failedAdmin)
