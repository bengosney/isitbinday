# Django
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path

# Third Party
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

# First Party
from books.urls import router as book_router
from food.urls import router as food_router
from recipes.urls import router as recipes_router
from tasks.urls import router as task_router

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/tasks/", include(task_router.urls)),
    path("api/food/", include(food_router.urls)),
    path("api/books/", include(book_router.urls)),
    path("api/recipes/", include(recipes_router.urls)),
    path("api/auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("", lambda request: HttpResponse("Health: OK")),
]
