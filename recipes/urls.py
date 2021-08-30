# Django

# Third Party
from rest_framework import routers

# Locals
from . import api

router = routers.DefaultRouter()
router.register("ingredient", api.ingredientViewSet)
router.register("recipe", api.recipeViewSet)
router.register("unit", api.unitViewSet)
router.register("step", api.stepViewSet)
