# Django

# Third Party
from rest_framework import routers

# Locals
from .. import api

router = routers.DefaultRouter()
router.register("unit-of-measure", api.UnitOfMeasureViewSet, basename="unit-of-measure")
router.register("stock", api.StockViewSet, basename="stock")
router.register("category", api.CategoryViewSet, basename="category")
router.register("product", api.ProductViewSet, basename="product")
router.register("brand", api.BrandViewSet, basename="brand")
router.register("location", api.LocationViewSet, basename="location")

urlpatterns = router.urls
app_name = "food"
