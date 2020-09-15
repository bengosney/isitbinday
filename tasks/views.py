from tasks.models import Task, Sprint
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

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
        return Task.objects.filter(owner=user)

    @action(detail=True)
    def do(self, request, pk=None):
        task = self.get_object()
        status = True
        task.do()
        task.save()

        serializer = self.get_serializer(task)

        return Response({'task': serializer.data, 'status': status})

    @action(detail=True)
    def done(self, request, pk=None):
        task = self.get_object()
        status = True
        task.done()
        task.save()

        serializer = self.get_serializer(task)

        return Response({'task': serializer.data, 'status': status})

    @action(detail=True)
    def cancel(self, request, pk=None):
        task = self.get_object()
        status = True
        task.cancel()
        task.save()

        serializer = self.get_serializer(task)

        return Response({'task': serializer.data, 'status': status})

    @action(detail=False, methods=['POST'])
    def position(self, request):
        for pair in request.data.get('positions'):
            task = Task.objects.get(pk=pair.get('id'))
            task.position = pair.get('position')
            task.save()

        return Response({'ok': 'ok'})


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
