# Third Party
from rest_framework import filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema

# First Party
from isitbinday.viewsets import OwnedModelViewSet
from tasks.permissions import IsOwner

# Locals
from . import models, serializers


class BookBaseSchema(AutoSchema):
    def __init__(self, tags: list[str] | None = None, operation_id_base=None, component_name=None):
        tags = (tags or []) + ["Books"]
        super().__init__(tags, operation_id_base, component_name)


class BookBaseViewSet(OwnedModelViewSet):
    schema = BookBaseSchema()


class AuthorViewSet(BookBaseViewSet):
    """ViewSet for the author class."""

    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


class BookViewSet(BookBaseViewSet):
    """ViewSet for the book class."""

    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    filter_backends = [filters.SearchFilter]
    search_fields = [
        "title",
    ]

    @action(detail=False, url_path="lookup/(?P<isbn>[^/.]+)")
    def lookup(self, request, isbn):
        try:
            book = models.Book.get_or_lookup(isbn, owner=request.user)
        except Exception as e:
            return Response(f"{type(e).__name__}: {e}", status=status.HTTP_400_BAD_REQUEST)

        return Response({"title": book.title})
