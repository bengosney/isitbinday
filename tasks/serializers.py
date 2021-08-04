# Third Party
from rest_framework import serializers
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField

# Locals
from .models import Sprint, Task


class TaskSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "due_date",
            "effort",
            "blocked_by",
            "state",
            "tags",
            "created",
            "last_updated",
            "owner",
            "available_state_transitions",
            "position",
            "completed",
            "repeats",
            "previous_state",
        ]

    owner = serializers.ReadOnlyField(source="owner.username")
    completed = serializers.ReadOnlyField()
    state = serializers.ReadOnlyField()

    def to_internal_value(self, data):
        if data.get("due_date", None) == "":
            data.pop("due_date")
        return super().to_internal_value(data)


class SprintSerializer(serializers.HyperlinkedModelSerializer):
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

    owner = serializers.ReadOnlyField(source="owner.username")
