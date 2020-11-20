from rest_framework import viewsets, permissions

from . import serializers
from . import models


class categoryViewSet(viewsets.ModelViewSet):
    """ViewSet for the category class"""

    queryset = models.category.objects.all()
    serializer_class = serializers.categorySerializer
    permission_classes = [permissions.IsAuthenticated]


class productViewSet(viewsets.ModelViewSet):
    """ViewSet for the product class"""

    queryset = models.product.objects.all()
    serializer_class = serializers.productSerializer
    permission_classes = [permissions.IsAuthenticated]


class brandViewSet(viewsets.ModelViewSet):
    """ViewSet for the brand class"""

    queryset = models.brand.objects.all()
    serializer_class = serializers.brandSerializer
    permission_classes = [permissions.IsAuthenticated]
