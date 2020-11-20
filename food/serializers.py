from rest_framework import serializers

from . import models


class categorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.category
        fields = [
            "name",
            "last_updated",
            "created",
        ]

class productSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.product
        fields = [
            "name",
            "last_updated",
            "created",
            "code",
        ]

class brandSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.brand
        fields = [
            "name",
            "created",
            "last_updated",
        ]
