# Third Party
from rest_framework import routers

# Locals
from . import api

router = routers.DefaultRouter()
router.register("author", api.AuthorViewSet, basename="author")
router.register("book", api.BookViewSet, basename="book")
router.register("sync", api.SyncSettingsViewSet, basename="sync")
