# Django
from django.core.exceptions import PermissionDenied

# Third Party
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema

# First Party
from isitbinday.viewsets import OwnedModelViewSet
from tasks.permissions import IsOwner

# Locals
from . import models, serializers
from .extractors import SchemaOrg


class RecipeBaseSchema(AutoSchema):
    def __init__(self, tags: list[str] | None = None, operation_id_base=None, component_name=None):
        tags = (tags or []) + ["Recipes"]
        super().__init__(tags, operation_id_base, component_name)


class RecipeBaseViewSet(OwnedModelViewSet):
    schema = RecipeBaseSchema()


class IngredientViewSet(RecipeBaseViewSet):
    """ViewSet for the ingredient class."""

    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


class RecipeViewSet(RecipeBaseViewSet):
    """ViewSet for the recipe class."""

    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_field = "slug"

    @action(detail=False, methods=["post"])
    def from_url(self, request):
        user = request.user
        if user is None:
            raise PermissionDenied

        serializer = serializers.RecipeURLSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        extractor = SchemaOrg(user)
        found = extractor.extract(serializer.validated_data["url"])

        return Response({"found": found})


class UnitViewSet(RecipeBaseViewSet):
    """ViewSet for the unit class."""

    queryset = models.Unit.objects.all()
    serializer_class = serializers.UnitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


class StepViewSet(RecipeBaseViewSet):
    """ViewSet for the step class."""

    queryset = models.Step.objects.all()
    serializer_class = serializers.StepSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
