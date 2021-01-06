# Django
from django.contrib import admin

# Locals
from .models import AuthDetails, HomeGroup


class AuthDetailsAdmin(admin.ModelAdmin):
    pass


class HomeGroupAdmin(admin.ModelAdmin):
    pass


admin.site.register(AuthDetails, AuthDetailsAdmin)
admin.site.register(HomeGroup, HomeGroupAdmin)
