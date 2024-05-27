# Django
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

# Third Party
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

# First Party
from books.urls import router as book_router
from food.urls import router as food_router
from recipes.urls import router as recipes_router
from tasks.urls import router as task_router

API_TITLE = "Is it bin day"
API_DESCRIPTION = "Help organize what you need to do"
API_VERSION = "1.0.0"

context = {"schema_url": "openapi"}

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/tasks/", include(task_router.urls)),
    path("api/food/", include(food_router.urls)),
    path("api/books/", include(book_router.urls)),
    path("api/recipes/", include(recipes_router.urls)),
    path("api/auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/accounts/", include("accounts.urls.api", namespace="accounts-api")),
    path("admin/", admin.site.urls),
    path(
        "openapi/",
        get_schema_view(title=API_TITLE, description=API_DESCRIPTION, version=API_VERSION),
        name="openapi",
    ),
    path("swagger/", TemplateView.as_view(template_name="swagger-ui.html", extra_context=context), name="swagger-ui"),
    path("redoc/", TemplateView.as_view(template_name="redoc.html", extra_context=context), name="redoc"),
    path("", include("accounts.urls.urls")),
    path("accounts/", include("allauth.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
        path("__debug__/", include("debug_toolbar.urls")),
    ]
