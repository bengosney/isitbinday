# Third Party
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# First Party
from tasks.permissions import IsOwner

# Locals
from . import models, serializers


class AuthorViewSet(viewsets.ModelViewSet):
    """ViewSet for the author class."""

    # queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return models.Author.objects.authorize(self.request, action="retrieve")


class BookViewSet(viewsets.ModelViewSet):
    """ViewSet for the book class."""

    # queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    filter_backends = [filters.SearchFilter]
    search_fields = [
        "title",
    ]

    def get_queryset(self):
        return models.Book.objects.authorize(self.request, action="retrieve")

    @action(detail=False, url_path="lookup/(?P<isbn>[^/.]+)")
    def lookup(self, request, isbn=None):
        try:
            book = models.Book.get_or_lookup(isbn, owner=self.request.user)
        except Exception as e:
            return Response(f"{type(e).__name__}: {e}", status=status.HTTP_400_BAD_REQUEST)

        return Response({"title": book.title})
        # serializer = LookupSerializer(product)
        # return Response(serializer.data)


class SyncSettingsViewSet(viewsets.ModelViewSet):
    """ViewSet for the sync settings class."""

    queryset = models.SyncSetting.objects.all()
    serializer_class = serializers.SyncSettingSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return models.SyncSetting.objects.authorize(self.request, action="retrieve")
