# Django
from django.contrib import admin
from django.urls import include, path

# Third Party
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

# First Party
from food.urls import router as foodRouter
from tasks.urls import router as taskRouter
from userauth.urls import router as userAuthRouter

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/tasks/", include(taskRouter.urls), name="task_base"),
    path("api/food/", include(foodRouter.urls), name="food_base"),
    path("api/user/", include(userAuthRouter.urls), name="user_base"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),
]
