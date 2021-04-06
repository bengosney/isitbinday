# Third Party
from rest_framework import routers

# Locals
from . import api

router = routers.DefaultRouter()
router.register("author", api.authorViewSet, basename="author")
router.register("book", api.bookViewSet, basename="book")
