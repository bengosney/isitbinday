# Django

# Third Party
from rest_framework import serializers

# Locals
from . import models

# class LookupSerializer(serializers.Serializer):


class UnitOfMeasureSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UnitOfMeasure
        fields = [
            "name",
            "created",
            "last_updated",
        ]
        read_only_fields = [
            "last_updated",
            "created",
        ]


class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Stock
        fields = [
            "product",
            "expires",
            "location",
            "added",
            "quantity",
            "unit_of_measure",
            "last_updated",
            "created",
        ]
        read_only_fields = [
            "last_updated",
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
        read_only_fields = [
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
            "brand",
            "categories",
            "quantity",
            "unit_of_measure",
        ]
        read_only_fields = [
            "last_updated",
            "created",
        ]


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Brand
        fields = [
            "name",
            "created",
            "last_updated",
        ]
        read_only_fields = [
            "last_updated",
            "created",
        ]


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Location
        fields = [
            "temperature",
            "name",
            "created",
            "last_updated",
        ]
        read_only_fields = [
            "last_updated",
            "created",
        ]


class LookupSerializer(serializers.ModelSerializer):
    class Meta(ProductSerializer.Meta):
        read_only_fields = [f for f in ProductSerializer.Meta.fields if f != 'code']

    def create(self, validated_data):
        code = validated_data.get('code')
        return models.Product.lookup(code)
