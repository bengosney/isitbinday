# Django
from django.urls import path

# Locals
from . import api, views

api_patterns = [
    path("create/", api.UserCreate.as_view(), name="create"),
    path("activate/", api.UserActivate.as_view(), name="activate"),
]

url_patterns = [path("", views.dashboard, name="accounts/dashboard")]

app_name = "accounts"
