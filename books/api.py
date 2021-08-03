# Third Party
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# First Party
from tasks.permissions import IsOwner

# Locals
from . import models, serializers


class authorViewSet(viewsets.ModelViewSet):
    """ViewSet for the author class."""

    # queryset = models.Author.objects.all()
    serializer_class = serializers.authorSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return models.Author.objects.authorize(self.request, action="retrieve")


class bookViewSet(viewsets.ModelViewSet):
    """ViewSet for the book class."""

    # queryset = models.Book.objects.all()
    serializer_class = serializers.bookSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

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
