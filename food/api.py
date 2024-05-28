# Django

# Third Party
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Locals
from . import models, serializers
from .models import Location, Product
from .serializers import LookupSerializer, StockSerializer


class UnitOfMeasureViewSet(viewsets.ModelViewSet):
    """ViewSet for the UnitOfMeasure class."""

    queryset = models.UnitOfMeasure.objects.all()
    serializer_class = serializers.UnitOfMeasureSerializer
    permission_classes = [permissions.IsAuthenticated]


class StockViewSet(viewsets.ModelViewSet):
    """ViewSet for the Stock class."""

    serializer_class = serializers.StockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """This view should return a list of all stocks for the currently
        authenticated user."""

        return models.Stock.objects.authorize(self.request, action="retrieve")

    @action(detail=True)
    def consume(self, request, pk: int):
        quantity = request.query_params.get("quantity", None)

        stock = self.get_object()
        stock.consume(quantity=quantity)

        serializer = StockSerializer(stock)

        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for the Category class."""

    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for the Product class."""

    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    lookup_field = "code"

    @action(detail=True)
    def lookup(self, request, code=None):
        try:
            product = Product.get_or_lookup(code)
        except Exception as e:
            return Response(f"{type(e).__name__}: {e}", status=status.HTTP_400_BAD_REQUEST)

        serializer = LookupSerializer(product)
        return Response(serializer.data)

    @action(detail=True)
    def transfer_in(self, request, code: str):
        quantity = float(request.query_params.get("quantity", 1))
        expires = request.query_params.get("expires", None)
        location = request.query_params.get("location", Location.get_default())

        product = Product.get_or_lookup(code)
        if product.is_pack:
            quantity *= product.quantity
        stock = product.transfer_in(self.request.user, quantity, expires, location)
        serializer = StockSerializer(stock)

        return Response(serializer.data)


class BrandViewSet(viewsets.ModelViewSet):
    """ViewSet for the Brand class."""

    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer
    permission_classes = [permissions.IsAuthenticated]


class LocationViewSet(viewsets.ModelViewSet):
    """ViewSet for the Location class."""

    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer
    permission_classes = [permissions.IsAuthenticated]
