from .models import Task, Sprint
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import TaskSerializer, SprintSerializer
from tasks.permissions import IsOwner

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewws or edited
    """

    queryset = Task.objects.all().order_by('-created')
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SprintViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Sprints to be viewws or edited
    """

    queryset = Sprint.objects.all().order_by('-created')
    serializer_class = SprintSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    