# Django
from django.views import generic

# Locals
from . import forms, models


class householdListView(generic.ListView):
    model = models.household
    form_class = forms.householdForm


class householdCreateView(generic.CreateView):
    model = models.household
    form_class = forms.householdForm


class householdDetailView(generic.DetailView):
    model = models.household
    form_class = forms.householdForm


class householdUpdateView(generic.UpdateView):
    model = models.household
    form_class = forms.householdForm
    pk_url_kwarg = "pk"


class memberListView(generic.ListView):
    model = models.member
    form_class = forms.memberForm


class memberCreateView(generic.CreateView):
    model = models.member
    form_class = forms.memberForm


class memberDetailView(generic.DetailView):
    model = models.member
    form_class = forms.memberForm


class memberUpdateView(generic.UpdateView):
    model = models.member
    form_class = forms.memberForm
    pk_url_kwarg = "pk"
