# Django

# Third Party
from rest_framework import routers

# Locals
from . import views

router = routers.DefaultRouter()
router.register("unit-of-measure", views.UnitOfMeasureViewSet, basename="unit-of-measure")
router.register("stock", views.StockViewSet, basename="stock")
router.register("category", views.CategoryViewSet, basename="category")
router.register("product", views.ProductViewSet, basename="product")
router.register("brand", views.BrandViewSet, basename="brand")
router.register("location", views.LocationViewSet, basename="location")

urlpatterns = router.urls
app_name = "food"
