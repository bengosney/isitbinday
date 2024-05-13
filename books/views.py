# Django
from django.views import generic

# Locals
from . import forms, models


class AuthorListView(generic.ListView):
    model = models.Author
    form_class = forms.AuthorForm


class AuthorCreateView(generic.CreateView):
    model = models.Author
    form_class = forms.AuthorForm


class AuthorDetailView(generic.DetailView):
    model = models.Author
    form_class = forms.AuthorForm


class AuthorUpdateView(generic.UpdateView):
    model = models.Author
    form_class = forms.AuthorForm
    pk_url_kwarg = "pk"


class BookListView(generic.ListView):
    model = models.Book
    form_class = forms.BbookForm


class BookCreateView(generic.CreateView):
    model = models.Book
    form_class = forms.BbookForm


class BookDetailView(generic.DetailView):
    model = models.Book
    form_class = forms.BbookForm


class BookUpdateView(generic.UpdateView):
    model = models.Book
    form_class = forms.BbookForm
    pk_url_kwarg = "pk"
