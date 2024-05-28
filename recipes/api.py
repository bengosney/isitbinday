# Django
from django.core.exceptions import PermissionDenied

# Third Party
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema

# First Party
from tasks.permissions import IsOwner

# Locals
from . import models, serializers
from .extrators import SchemaOrg


class BaseViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return super().get_queryset().authorize(self.request, action="retrieve")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class IngredientViewSet(BaseViewSet):
    """ViewSet for the ingredient class."""

    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


class RecipeSchema(AutoSchema):
    def get_operation_id(self, path: str, method: str):
        postfix = ""
        if path.strip("/").split("/")[-1] == "from_url":
            postfix = method.capitalize()

        return f"{super().get_operation_id(path, method)}{postfix}"


class RecipeViewSet(BaseViewSet):
    """ViewSet for the recipe class."""

    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_field = "slug"
    schema = RecipeSchema()

    @action(detail=False, methods=["put", "post"])
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


class UnitViewSet(BaseViewSet):
    """ViewSet for the unit class."""

    queryset = models.Unit.objects.all()
    serializer_class = serializers.UnitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


class StepViewSet(BaseViewSet):
    """ViewSet for the step class."""

    queryset = models.Step.objects.all()
    serializer_class = serializers.StepSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
