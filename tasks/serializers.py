# Third Party
from rest_framework import serializers

# Locals
from .models import Sprint, Task


class TaskSerializer(serializers.HyperlinkedModelSerializer):

    owner = serializers.ReadOnlyField(source="owner.username")
    completed = serializers.ReadOnlyField()
    state = serializers.ReadOnlyField()

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "due_date",
            "effort",
            "blocked_by",
            "state",
            "created",
            "last_updated",
            "owner",
            "available_state_transitions",
            "position",
            "completed",
            "repeats",
            "previous_state",
        ]

    def to_internal_value(self, data):
        if data.get("due_date", None) == "":
            data.pop("due_date")
        return super().to_internal_value(data)


class SprintSerializer(serializers.HyperlinkedModelSerializer):

    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Sprint
        fields = [
            "id",
            "title",
            "state",
            "started",
            "finished",
            "tasks",
            "created",
            "last_updated",
            "owner",
        ]
