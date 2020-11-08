# Third Party
from rest_framework import serializers

# Locals
from .models import Sprint, Task


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
            'previous_state',
        ]

    owner = serializers.ReadOnlyField(source='owner.username')
    completed = serializers.ReadOnlyField()
    state = serializers.ReadOnlyField()


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
