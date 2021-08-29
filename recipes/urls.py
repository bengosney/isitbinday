# Django
from django.urls import include, path

# Third Party
from rest_framework import routers

# Locals
from . import api, views

router = routers.DefaultRouter()
router.register("ingredient", api.ingredientViewSet)
router.register("recipe", api.recipeViewSet)
router.register("unit", api.unitViewSet)
router.register("step", api.stepViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("recipes/ingredient/", views.ingredientListView.as_view(), name="recipes_ingredient_list"),
    path("recipes/ingredient/create/", views.ingredientCreateView.as_view(), name="recipes_ingredient_create"),
    path("recipes/ingredient/detail/<int:pk>/", views.ingredientDetailView.as_view(), name="recipes_ingredient_detail"),
    path("recipes/ingredient/update/<int:pk>/", views.ingredientUpdateView.as_view(), name="recipes_ingredient_update"),
    path("recipes/recipe/", views.recipeListView.as_view(), name="recipes_recipe_list"),
    path("recipes/recipe/create/", views.recipeCreateView.as_view(), name="recipes_recipe_create"),
    path("recipes/recipe/detail/<int:pk>/", views.recipeDetailView.as_view(), name="recipes_recipe_detail"),
    path("recipes/recipe/update/<int:pk>/", views.recipeUpdateView.as_view(), name="recipes_recipe_update"),
    path("recipes/unit/", views.unitListView.as_view(), name="recipes_unit_list"),
    path("recipes/unit/create/", views.unitCreateView.as_view(), name="recipes_unit_create"),
    path("recipes/unit/detail/<int:pk>/", views.unitDetailView.as_view(), name="recipes_unit_detail"),
    path("recipes/unit/update/<int:pk>/", views.unitUpdateView.as_view(), name="recipes_unit_update"),
    path("recipes/step/", views.stepListView.as_view(), name="recipes_step_list"),
    path("recipes/step/create/", views.stepCreateView.as_view(), name="recipes_step_create"),
    path("recipes/step/detail/<int:pk>/", views.stepDetailView.as_view(), name="recipes_step_detail"),
    path("recipes/step/update/<int:pk>/", views.stepUpdateView.as_view(), name="recipes_step_update"),
)
