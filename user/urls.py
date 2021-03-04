# Django
from django.urls import path

# Locals
from . import views

urlpatterns = [
    path("create/", views.UserCreate.as_view(), name="create"),
]

app_name = "user"
