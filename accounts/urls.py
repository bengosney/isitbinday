# Django
from django.urls import path

# Locals
from . import views

urlpatterns = [
    path("create/", views.UserCreate.as_view(), name="create"),
    path("activate/", views.UserActivate.as_view(), name="activate"),
]

app_name = "accounts"
