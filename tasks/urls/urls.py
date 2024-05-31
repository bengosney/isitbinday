# Django
from django.urls import path

# Locals
from .. import views

app_name = "tasks"
urlpatterns = [path("", views.TaskListView.as_view(), name="list")]
