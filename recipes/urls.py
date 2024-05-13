# Django

# Third Party
from rest_framework import routers

# Locals
from . import api

router = routers.DefaultRouter()
router.register("ingredient", api.IngredientViewSet)
router.register("recipe", api.RecipeViewSet)
router.register("unit", api.UnitViewSet)
router.register("step", api.StepViewSet)
