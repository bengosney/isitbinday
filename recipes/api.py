# Third Party
from rest_framework import permissions, viewsets

# First Party
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
