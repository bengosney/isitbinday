# Django
from django.contrib import admin

# First Party
from utils.admin import AutoFieldsAdminMixin

# Locals
from .models import HomeGroup


@admin.register(HomeGroup)
class HomeGroupAdmin(AutoFieldsAdminMixin, admin.ModelAdmin):
    pass
