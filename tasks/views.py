# Standard Library
from collections import defaultdict
from datetime import date, datetime, timedelta

# Third Party
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# First Party
from tasks.models import Sprint, Task
from tasks.permissions import IsOwner

# Locals
from .serializers import SprintSerializer, TaskSerializer


class ArchiveTaskListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that shows a list of archived tasks
    """

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        """
        This view should return a list of archived tasks for the currently authenticated user.
        """

        return Task.objects.authorize(self.request, action="retrieve")


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be views or edited
    """

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        This view should return a list of all tasks for the currently authenticated user.
        """
        
        return Task.objects.authorize(self.request, action="retrieve").exclude(state=Task.STATE_ARCHIVE).filter(show_after__lte=datetime.today().date())

    @action(detail=True)
    def todo(self, request, pk=None):
        task = self.get_object()
        status = True
        task.todo()
        task.save()

        serializer = self.get_serializer(task)

        return Response({'task': serializer.data, 'status': status})

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
    def due_date_states(self, request):
        return Response({'states': [s for s in Task.STATES_DUE_DATE_MATTERS]})

    @action(detail=False)
    def auto_archive(self, request):
        days = int(request.query_params.get('days', 5))
        before = date.today() - timedelta(days=days)

        count = Task.auto_archive(before)

        return Response({'ok': True, 'count': count, 'before': before})


class SprintViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Sprints to be views or edited
    """

    serializer_class = SprintSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        This view should return a list of all tasks for the currently authenticated user.
        """

        return Sprint.objects.authorize(self.request, action="retrieve").order_by('-created')
