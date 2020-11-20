from rest_framework import serializers

from . import models


class UnitOfMeasureSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UnitOfMeasure
        fields = [
            "name",
            "created",
            "last_updated",
        ]

class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Stock
        fields = [
            "last_updated",
            "added",
            "quantity",
            "created",
        ]

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = [
            "name",
            "last_updated",
            "created",
        ]

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = [
            "name",
            "last_updated",
            "created",
            "code",
        ]

class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Brand
        fields = [
            "name",
            "created",
            "last_updated",
        ]

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Location
        fields = [
            "type",
            "name",
            "created",
            "last_updated",
        ]
