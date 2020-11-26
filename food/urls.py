# Django

# Third Party
from rest_framework import routers

# Locals
from . import views

router = routers.DefaultRouter()
router.register("unit-of-measure", views.UnitOfMeasureViewSet)
router.register("stock", views.StockViewSet)
router.register("category", views.CategoryViewSet)
router.register("product", views.ProductViewSet)
router.register("brand", views.BrandViewSet)
router.register("location", views.LocationViewSet)
