# Django
from django.urls import include, path

# Third Party
from rest_framework import routers

# Locals
from . import api, views

router = routers.DefaultRouter()
router.register("unit-of-measure", api.UnitOfMeasureViewSet)
router.register("stock", api.StockViewSet)
router.register("category", api.CategoryViewSet)
router.register("product", api.ProductViewSet)
router.register("brand", api.BrandViewSet)
router.register("location", api.LocationViewSet)

