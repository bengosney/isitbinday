# Third Party
from rest_framework import serializers

# Locals
from . import models


class SyncSettingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.SyncSetting
        fields = [
            "id",
            "server",
            "database",
            "username",
            "password",
            "last_sync",
        ]
        extra_kwargs = {"password": {"write_only": True}}


class SimpleAuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Author
        fields = [
            "id",
            "name",
        ]


class SimpleBookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Book
        fields = [
            "id",
            "title",
        ]


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Author
        fields = [
            "name",
            "created",
            "last_updated",
            "books",
        ]

    books = SimpleBookSerializer(many=True, read_only=True)


class BookSerializer(serializers.HyperlinkedModelSerializer):
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

    authors = SimpleAuthorSerializer(many=True, read_only=True)
