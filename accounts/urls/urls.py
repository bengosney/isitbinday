# Django
from django.urls import path

# Locals
from .. import views

app_name = "accounts"
urlpatterns = [path("", views.dashboard, name="dashboard")]
