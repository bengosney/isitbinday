# Django
from django.urls import include, path

# Third Party
from rest_framework import routers

# Locals
from . import api, views

router = routers.DefaultRouter()
router.register("UnitOfMeasure", api.UnitOfMeasureViewSet)
router.register("Stock", api.StockViewSet)
router.register("Category", api.CategoryViewSet)
router.register("Product", api.ProductViewSet)
router.register("Brand", api.BrandViewSet)
router.register("Location", api.LocationViewSet)

urlpatterns = (
    path('<str:code>', views.LookupProduct),
    path("api/v1/", include(router.urls)),
)
