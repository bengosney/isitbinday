# Django
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

# Third Party
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

# First Party
from accounts.urls import urlpatterns as user_urls
from food.urls import router as foodRouter
from tasks.urls import router as taskRouter

API_TITLE = "Is it bin day"
API_DESCRIPTION = "Help organise what you need to do"
API_VERSION = "1.0.0"

APT_DETAILS = {
    "title": API_TITLE,
    "description": API_DESCRIPTION,
    "version": API_VERSION,
}

context = {"schema_url": "openapi-schema"}

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/tasks/", include(taskRouter.urls)),
    path("api/food/", include(foodRouter.urls)),
    path("api/auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/accounts/", include(user_urls)),
    path("admin/", admin.site.urls),
    path("openapi/", get_schema_view(**APT_DETAILS), name="openapi-schema"),
    path("swagger/", TemplateView.as_view(template_name="swagger-ui.html", extra_context=context), name="swagger-ui"),
    path("redoc/", TemplateView.as_view(template_name="redoc.html", extra_context=context), name="redoc"),
]
