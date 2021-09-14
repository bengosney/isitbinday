# Third Party
from rest_framework import serializers

# Locals
from . import models


class baseSerializerMeta:
    exclude = ("owner",)
    read_only_fields = (
        "last_updated",
        "created",
    )
    owner = serializers.ReadOnlyField(source="owner.username")


class ingredientSerializer(serializers.ModelSerializer):
    quantity_metric = serializers.FloatField(read_only=True)
    quantity_metric_unit = serializers.CharField(read_only=True)

    class Meta(baseSerializerMeta):
        model = models.Ingredient


class unitSerializer(serializers.ModelSerializer):
    class Meta(baseSerializerMeta):
        model = models.Unit


class stepSerializer(serializers.ModelSerializer):
    class Meta(baseSerializerMeta):
        model = models.Step


class recipeSerializer(serializers.ModelSerializer):
    ingredients = ingredientSerializer(many=True, required=False)
    steps = stepSerializer(many=True, required=False)

    class Meta(baseSerializerMeta):
        model = models.Recipe
        depth = 1
