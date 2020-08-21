from rest_framework import serializers
from .models import Task, Sprint


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = [
            'title',
            'due_date',
            'effort',
            'blocked_by',
            'state',
            'created',
            'last_updated',
        ]


class SprintSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sprint
        fields = [
            'title',
            'state',
            'started',
            'finished',
            'tasks',
            'created',
            'last_updated',
        ]
