# Django

# Third Party
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema

# First Party
from isitbinday.viewsets import OwnedModelViewSet

# Locals
from . import models, serializers
from .models import Location, Product
from .serializers import LookupSerializer, StockSerializer


class FoodBaseSchema(AutoSchema):
    def __init__(self, tags: list[str] | None = None, operation_id_base=None, component_name=None):
        tags = (tags or []) + ["Food"]
        super().__init__(tags, operation_id_base, component_name)


class FoodBaseViewSet(OwnedModelViewSet):
    schema = FoodBaseSchema()


class UnitOfMeasureViewSet(viewsets.ModelViewSet):
    """ViewSet for the UnitOfMeasure class."""

    queryset = models.UnitOfMeasure.objects.all()
    serializer_class = serializers.UnitOfMeasureSerializer
    permission_classes = [permissions.IsAuthenticated]
    schema = FoodBaseSchema()


class StockViewSet(FoodBaseViewSet):
    """ViewSet for the Stock class."""

    queryset = models.Stock.objects.all()
    serializer_class = serializers.StockSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True)
    def consume(self, request, pk: int):
        quantity = request.query_params.get("quantity", None)

        stock = self.get_object()
        stock.consume(quantity=quantity)

        serializer = StockSerializer(stock)

        return Response(serializer.data)


class CategoryViewSet(FoodBaseViewSet):
    """ViewSet for the Category class."""

    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductViewSet(FoodBaseViewSet):
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


class BrandViewSet(FoodBaseViewSet):
    """ViewSet for the Brand class."""

    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer
    permission_classes = [permissions.IsAuthenticated]


class LocationViewSet(FoodBaseViewSet):
    """ViewSet for the Location class."""

    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer
    permission_classes = [permissions.IsAuthenticated]
