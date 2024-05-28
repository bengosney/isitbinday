# Third Party
from rest_framework import routers

# Locals
from .views import ArchiveTaskListView, SprintViewSet, TaskViewSet

router = routers.DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")
router.register(r"archived-tasks", ArchiveTaskListView, basename="archived-tasks")
router.register(r"sprints", SprintViewSet, basename="sprint")

urlpatterns = router.urls
app_name = "tasks"
