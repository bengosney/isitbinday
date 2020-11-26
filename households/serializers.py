# Third Party
from rest_framework import serializers

# Locals
from . import models


class householdSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.household
        fields = [
            "created",
            "last_updated",
            "name",
        ]


class memberSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.member
        fields = [
            "level",
            "created",
            "last_updated",
        ]
