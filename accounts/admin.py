# Django
from django.contrib import admin

# Locals
from .models import HomeGroup


@admin.register(HomeGroup)
class HomeGroupAdmin(admin.ModelAdmin):
    list_display = [field.name for field in HomeGroup._meta.fields]
    search_fields = [
        field.name for field in HomeGroup._meta.fields if field.get_internal_type() in ["CharField", "TextField"]
    ]
    list_filter = [
        field.name
        for field in HomeGroup._meta.fields
        if field.get_internal_type() in ["BooleanField", "DateField", "DateTimeField"]
    ]
