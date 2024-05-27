# Django
from django.urls import path

# Locals
from .. import api

app_name = "accounts"

urlpatterns = [
    path("create/", api.UserCreate.as_view(), name="create"),
    path("activate/", api.UserActivate.as_view(), name="activate"),
]
