# Third Party
from rest_framework import routers

# Locals
from .views import HomeGroupViewSet, UserProfileViewSet

router = routers.DefaultRouter()
router.register(r"profile", UserProfileViewSet, basename="profile")
router.register(r"homegroup", HomeGroupViewSet, basename="homegroup")
