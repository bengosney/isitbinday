# Third Party
from rest_framework import routers

# Locals
from .views import SprintViewSet, TaskViewSet, ArchiveTaskListView



router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'archivetasks', ArchiveTaskListView, basename='archivetask')
router.register(r'sprints', SprintViewSet, basename='sprint')
