# Third Party
from rest_framework import serializers

# Locals
from . import models


class simpleAuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Author
        fields = [
            "id",
            "name",
        ]


class simpleBookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Book
        fields = [
            "id",
            "title",
        ]


class authorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Author
        fields = [
            "name",
            "created",
            "last_updated",
            "books",
        ]

    books = simpleBookSerializer(many=True, read_only=True)


class bookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Book
        fields = [
            "id",
            "publish_date",
            "title",
            "isbn",
            "last_updated",
            "created",
            "authors",
            "tmp_cover",
        ]

    authors = simpleAuthorSerializer(many=True, read_only=True)
