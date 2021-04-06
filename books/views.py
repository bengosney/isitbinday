# Django
from django.views import generic

# Locals
from . import forms, models


class authorListView(generic.ListView):
    model = models.Author
    form_class = forms.authorForm


class authorCreateView(generic.CreateView):
    model = models.Author
    form_class = forms.authorForm


class authorDetailView(generic.DetailView):
    model = models.Author
    form_class = forms.authorForm


class authorUpdateView(generic.UpdateView):
    model = models.Author
    form_class = forms.authorForm
    pk_url_kwarg = "pk"


class bookListView(generic.ListView):
    model = models.Book
    form_class = forms.bookForm


class bookCreateView(generic.CreateView):
    model = models.Book
    form_class = forms.bookForm


class bookDetailView(generic.DetailView):
    model = models.Book
    form_class = forms.bookForm


class bookUpdateView(generic.UpdateView):
    model = models.Book
    form_class = forms.bookForm
    pk_url_kwarg = "pk"
