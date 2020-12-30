# Django
from django.contrib import admin

# Locals
from .models import AuthDetails


class AuthDetailsAdmin(admin.ModelAdmin):
    pass


admin.site.register(AuthDetails, AuthDetailsAdmin)
