# Django
from django.http.response import Http404

# Third Party
import openfoodfacts
from googletrans import Translator
from rest_framework import serializers

# Locals
from . import models

# class LookupSerializer(serializers.Serializer):


class LookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = [
            "name",
            "last_updated",
            "created",
            "code",
            "brand",
            "categories",
        ]
        read_only_fields = [
            "name",
            "last_updated",
            "created",
            "brand",
            "categories",
        ]

    def create(self, validated_data):
        code = validated_data.get('code')
        try:
            product = openfoodfacts.products.get_product(code)['product']
        except KeyError:
            raise Http404(f'{code} not found')

        name = None
        for key in ['generic_name', 'product_name']:
            try:
                name = product[key]
            except KeyError:
                pass

        categories = product['categories'].split(',')
        if product['categories_lc'] != 'en':
            try:
                translator = Translator()
                categories = [c.text for c in translator.translate(categories, src=product['categories_lc'], dest='en')]
            except BaseException:
                categories = []

        if name is None:
            raise Http404('Name not found')

        return models.Product.get_or_create(code, name, product['brands'], filter(None, categories))


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
