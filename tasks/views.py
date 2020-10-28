from tasks.models import Task, Sprint
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import TaskSerializer, SprintSerializer
from tasks.permissions import IsOwner

from collections import defaultdict
from pprint import pprint


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

    @action(detail=True)
    def archive(self, request, pk=None):
        task = self.get_object()
        task.archive()
        task.save()

        serializer = self.get_serializer(task)

        return Response({'task': serializer.data, 'status': True})

    @action(detail=False, methods=['POST'])
    def position(self, request):
        for pair in request.data.get('positions'):
            task = Task.objects.get(pk=pair.get('id'))
            task.position = pair.get('position')
            task.save()

        return Response({'ok': 'ok'})

    @action(detail=False)
    def transitions(self, request):
        task = Task()
        transitions = defaultdict(lambda: {
            'sources': set(),
            'target': '',
            'name': ''
        })

        for t in task.get_all_state_transitions():
            transitions[t.target]['sources'].add(t.source)
            transitions[t.target]['target'] = t.target
            transitions[t.target]['name'] = t.name

        return Response({'transitions': [transitions[t] for t in Task.STATES]})

    def _all_states(self):
        task = Task()
        states = defaultdict(lambda: {
            'sources': set(),
            'transitions': set(),
            'destination': set(),
            'name': '',
        })

        for state in Task.STATES:
            states[state]['name'] = state

        for t in task.get_all_state_transitions():
            states[t.target]['sources'].add(t.source)
            states[t.source]['destination'].add(t.target)
            states[t.target]['transitions'].add(t.name)

        return [states[s] for s in states if states[s]['name'] != '']

    @action(detail=False)
    def states(self, request):
        return Response({'states': [s for s in self._all_states() if s['name'] not in Task.HIDDEN_STATES]})

    @action(detail=False)
    def hidden_states(self, request):
        return Response({'states': [s for s in self._all_states() if s['name'] in Task.HIDDEN_STATES]})

    @action(detail=False)
    def auto_archive(self, request):
        Task.auto_archive(1)
        return Response({'ok': True})


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
