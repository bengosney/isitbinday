# Third Party
from rest_framework import serializers

# Locals
from . import models

defaultExcludes = (
    "owner",
    "last_updated",
    "created",
    "temperature",
    "temperature_changed",
)


class UnitOfMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UnitOfMeasure
        exclude = [f for f in defaultExcludes if getattr(models.UnitOfMeasure, f, False)]


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Stock
        exclude = [f for f in defaultExcludes if getattr(models.Stock, f, False)]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        exclude = [f for f in defaultExcludes if getattr(models.Category, f, False)]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        exclude = [f for f in defaultExcludes if getattr(models.Product, f, False)]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        exclude = [f for f in defaultExcludes if getattr(models.Brand, f, False)]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        exclude = [f for f in defaultExcludes if getattr(models.Location, f, False)]


class LookupSerializer(serializers.ModelSerializer):
    class Meta(ProductSerializer.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != "code":
                self.fields[field].read_only = True

    def create(self, validated_data):
        code = validated_data.get("code")
        return models.Product.lookup(code)
