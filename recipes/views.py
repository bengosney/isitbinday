# Django
from django.views import generic

# Locals
from . import forms, models


class ingredientListView(generic.ListView):
    model = models.ingredient
    form_class = forms.ingredientForm


class ingredientCreateView(generic.CreateView):
    model = models.ingredient
    form_class = forms.ingredientForm


class ingredientDetailView(generic.DetailView):
    model = models.ingredient
    form_class = forms.ingredientForm


class ingredientUpdateView(generic.UpdateView):
    model = models.ingredient
    form_class = forms.ingredientForm
    pk_url_kwarg = "pk"


class recipeListView(generic.ListView):
    model = models.recipe
    form_class = forms.recipeForm


class recipeCreateView(generic.CreateView):
    model = models.recipe
    form_class = forms.recipeForm


class recipeDetailView(generic.DetailView):
    model = models.recipe
    form_class = forms.recipeForm


class recipeUpdateView(generic.UpdateView):
    model = models.recipe
    form_class = forms.recipeForm
    pk_url_kwarg = "pk"


class unitListView(generic.ListView):
    model = models.unit
    form_class = forms.unitForm


class unitCreateView(generic.CreateView):
    model = models.unit
    form_class = forms.unitForm


class unitDetailView(generic.DetailView):
    model = models.unit
    form_class = forms.unitForm


class unitUpdateView(generic.UpdateView):
    model = models.unit
    form_class = forms.unitForm
    pk_url_kwarg = "pk"


class stepListView(generic.ListView):
    model = models.step
    form_class = forms.stepForm


class stepCreateView(generic.CreateView):
    model = models.step
    form_class = forms.stepForm


class stepDetailView(generic.DetailView):
    model = models.step
    form_class = forms.stepForm


class stepUpdateView(generic.UpdateView):
    model = models.step
    form_class = forms.stepForm
    pk_url_kwarg = "pk"
