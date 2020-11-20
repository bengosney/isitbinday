from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


router = routers.DefaultRouter()
router.register("UnitOfMeasure", api.UnitOfMeasureViewSet)
router.register("Stock", api.StockViewSet)
router.register("Category", api.CategoryViewSet)
router.register("Product", api.ProductViewSet)
router.register("Brand", api.BrandViewSet)
router.register("Location", api.LocationViewSet)

urlpatterns = (
    path('', views.test),
    path("api/v1/", include(router.urls)),
)
