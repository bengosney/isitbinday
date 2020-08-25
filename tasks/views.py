from .models import Task, Sprint
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import TaskSerializer, SprintSerializer
from tasks.permissions import IsOwner

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewws or edited
    """

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        This view should return a list of all tasks for the currently authenticated user.
        """
        user = self.request.user
        return Task.objects.filter(owner=user).order_by('-created')


class SprintViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Sprints to be viewws or edited
    """

    serializer_class = SprintSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        This view should return a list of all tasks for the currently authenticated user.
        """
        user = self.request.user
        return Sprint.objects.filter(owner=user).order_by('-created')