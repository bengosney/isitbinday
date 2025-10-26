# Django
from django.urls import path

# Locals
from . import views

urlpatterns = [
    path("create/", views.UserCreate.as_view(), name="create"),
    path("activate/", views.UserActivate.as_view(), name="activate"),
    path("google-login/", views.GoogleJWTLogin.as_view(), name="google-login"),
]

app_name = "accounts"
