from rest_framework import serializers
from .models import Task, Sprint
from django.contrib.auth.models import User


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'due_date',
            'effort',
            'blocked_by',
            'state',
            'created',
            'last_updated',
            'owner',
            'available_state_transitions',
            'position',
            'completed',
            'repeats',
        ]

    owner = serializers.ReadOnlyField(source='owner.username')
    completed = serializers.ReadOnlyField()


    


class SprintSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sprint
        fields = [
            'id',
            'title',
            'state',
            'started',
            'finished',
            'tasks',
            'created',
            'last_updated',
            'owner',
        ]

    owner = serializers.ReadOnlyField(source='owner.username')


