# Third Party
from rest_framework import routers

# Locals
from .views import SprintViewSet, TaskViewSet, ArchiveTaskListView



router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'archived-tasks', ArchiveTaskListView, basename='archived-tasks')
router.register(r'sprints', SprintViewSet, basename='sprint')
