from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


router = routers.DefaultRouter()
router.register("category", api.categoryViewSet)
router.register("product", api.productViewSet)
router.register("brand", api.brandViewSet)

urlpatterns = (
    path('', views.test),
    path("api/v1/", include(router.urls)),
    path("category/", views.categoryListView.as_view(), name="food_category_list"),
    path("category/create/", views.categoryCreateView.as_view(), name="food_category_create"),
    path("category/detail/<int:pk>/", views.categoryDetailView.as_view(), name="food_category_detail"),
    path("category/update/<int:pk>/", views.categoryUpdateView.as_view(), name="food_category_update"),
    path("product/", views.productListView.as_view(), name="food_product_list"),
    path("product/create/", views.productCreateView.as_view(), name="food_product_create"),
    path("product/detail/<int:pk>/", views.productDetailView.as_view(), name="food_product_detail"),
    path("product/update/<int:pk>/", views.productUpdateView.as_view(), name="food_product_update"),
    path("brand/", views.brandListView.as_view(), name="food_brand_list"),
    path("brand/create/", views.brandCreateView.as_view(), name="food_brand_create"),
    path("brand/detail/<int:pk>/", views.brandDetailView.as_view(), name="food_brand_detail"),
    path("brand/update/<int:pk>/", views.brandUpdateView.as_view(), name="food_brand_update"),
)
