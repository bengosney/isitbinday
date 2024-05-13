# Django
from django.views import generic

# Locals
from . import forms, models


class IngredientListView(generic.ListView):
    model = models.Ingredient
    form_class = forms.IngredientForm


class IngredientCreateView(generic.CreateView):
    model = models.Ingredient
    form_class = forms.IngredientForm


class IngredientDetailView(generic.DetailView):
    model = models.Ingredient
    form_class = forms.IngredientForm


class IngredientUpdateView(generic.UpdateView):
    model = models.Ingredient
    form_class = forms.IngredientForm
    pk_url_kwarg = "pk"


class RecipeListView(generic.ListView):
    model = models.Recipe
    form_class = forms.RecipeForm


class RecipeCreateView(generic.CreateView):
    model = models.Recipe
    form_class = forms.RecipeForm


class RecipeDetailView(generic.DetailView):
    model = models.Recipe
    form_class = forms.RecipeForm


class RecipeUpdateView(generic.UpdateView):
    model = models.Recipe
    form_class = forms.RecipeForm
    pk_url_kwarg = "pk"


class UnitListView(generic.ListView):
    model = models.Unit
    form_class = forms.UnitForm


class UnitCreateView(generic.CreateView):
    model = models.Unit
    form_class = forms.UnitForm


class UnitDetailView(generic.DetailView):
    model = models.Unit
    form_class = forms.UnitForm


class UnitUpdateView(generic.UpdateView):
    model = models.Unit
    form_class = forms.UnitForm
    pk_url_kwarg = "pk"


class StepListView(generic.ListView):
    model = models.Step
    form_class = forms.StepForm


class StepCreateView(generic.CreateView):
    model = models.Step
    form_class = forms.StepForm


class StepDetailView(generic.DetailView):
    model = models.Step
    form_class = forms.StepForm


class StepUpdateView(generic.UpdateView):
    model = models.Step
    form_class = forms.StepForm
    pk_url_kwarg = "pk"
