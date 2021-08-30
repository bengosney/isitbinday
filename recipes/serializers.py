# Third Party
from rest_framework import serializers

# Locals
from . import models


class ingredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ingredient
        fields = [
            "name",
            "last_updated",
            "created",
            "quantity",
        ]


class recipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.recipe
        fields = [
            "name",
            "time",
            "description",
            "ingredients",
            "steps",
            "last_updated",
            "link",
            "created",
        ]


class unitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.unit
        fields = [
            "created",
            "last_updated",
            "name",
        ]


class stepSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.step
        fields = [
            "created",
            "last_updated",
            "description",
        ]
