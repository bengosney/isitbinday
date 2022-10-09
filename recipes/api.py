# Django
from django.core.exceptions import PermissionDenied

# Third Party
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# First Party
from recipes.extrators import schema_org
from tasks.permissions import IsOwner

# Locals
from . import models, serializers


class baseViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return super().get_queryset().authorize(self.request, action="retrieve")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ingredientViewSet(baseViewSet):
    """ViewSet for the ingredient class."""

    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.ingredientSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


class recipeViewSet(baseViewSet):
    """ViewSet for the recipe class."""

    queryset = models.Recipe.objects.all()
    serializer_class = serializers.recipeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_field = "slug"

    @action(detail=False, methods=["put", "post"])
    def from_url(self, request):
        user = request.user
        if user is None:
            raise PermissionDenied

        serializer = serializers.recipeURLSerializer(data=request.data)
        if serializer.is_valid():
            extractor = schema_org(user)
            found = extractor.extract(serializer.validated_data["url"])

            return Response({"found": found})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class unitViewSet(baseViewSet):
    """ViewSet for the unit class."""

    queryset = models.Unit.objects.all()
    serializer_class = serializers.unitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


class stepViewSet(baseViewSet):
    """ViewSet for the step class."""

    queryset = models.Step.objects.all()
    serializer_class = serializers.stepSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
