# Third Party
from rest_framework import serializers

# Locals
from . import models


class BaseSerializerMeta:
    exclude = ("owner",)
    read_only_fields = (
        "last_updated",
        "created",
    )
    owner = serializers.ReadOnlyField(source="owner.username")


class IngredientSerializer(serializers.ModelSerializer):
    class Meta(BaseSerializerMeta):
        model = models.Ingredient

    quantity_unit = serializers.CharField(read_only=True)
    quantity_metric = serializers.FloatField(read_only=True)
    quantity_metric_unit = serializers.CharField(read_only=True)


class UnitSerializer(serializers.ModelSerializer):
    class Meta(BaseSerializerMeta):
        model = models.Unit


class StepSerializer(serializers.ModelSerializer):
    class Meta(BaseSerializerMeta):
        model = models.Step


class RecipeSerializer(serializers.ModelSerializer):
    class Meta(BaseSerializerMeta):
        model = models.Recipe
        depth = 1

    ingredients = IngredientSerializer(many=True, required=False)
    steps = StepSerializer(many=True, required=False)


class RecipeURLSerializer(serializers.Serializer):
    url = serializers.URLField()
