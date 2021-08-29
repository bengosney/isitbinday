# Third Party
from rest_framework import permissions, viewsets

# Locals
from . import models, serializers


class ingredientViewSet(viewsets.ModelViewSet):
    """ViewSet for the ingredient class."""

    queryset = models.ingredient.objects.all()
    serializer_class = serializers.ingredientSerializer
    permission_classes = [permissions.IsAuthenticated]


class recipeViewSet(viewsets.ModelViewSet):
    """ViewSet for the recipe class."""

    queryset = models.recipe.objects.all()
    serializer_class = serializers.recipeSerializer
    permission_classes = [permissions.IsAuthenticated]


class unitViewSet(viewsets.ModelViewSet):
    """ViewSet for the unit class."""

    queryset = models.unit.objects.all()
    serializer_class = serializers.unitSerializer
    permission_classes = [permissions.IsAuthenticated]


class stepViewSet(viewsets.ModelViewSet):
    """ViewSet for the step class."""

    queryset = models.step.objects.all()
    serializer_class = serializers.stepSerializer
    permission_classes = [permissions.IsAuthenticated]
