from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from tasks.views import TaskViewSet, SprintViewSet

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'sprints', SprintViewSet, basename='sprint')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
