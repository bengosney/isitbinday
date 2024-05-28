# Third Party
from rest_framework import routers

# Locals
from .. import api

router = routers.DefaultRouter()
router.register(r"tasks", api.TaskViewSet, basename="task")
router.register(r"archived-tasks", api.ArchiveTaskListView, basename="archived-tasks")
router.register(r"sprints", api.SprintViewSet, basename="sprint")

urlpatterns = router.urls
app_name = "tasks"
