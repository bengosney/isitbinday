from django.views import generic
from . import models
from . import forms

from django.http import HttpResponse
import openfoodfacts
from pprint import pprint, pformat


def test(request):
    code = '5010024111069'
    product = openfoodfacts.products.get_product(code)['product']

    bob = ''
    #bob = f"name: {product['generic_name']}<br />brand: {product['brands']} <br />categories: {product['categories']}"
    obj = models.product.get_or_create(code, product['generic_name'], product['brands'], product['categories'])
    return HttpResponse(f'{bob}<pre>{pformat(product)}</pre>')


class categoryListView(generic.ListView):
    model = models.category
    form_class = forms.categoryForm


class categoryCreateView(generic.CreateView):
    model = models.category
    form_class = forms.categoryForm


class categoryDetailView(generic.DetailView):
    model = models.category
    form_class = forms.categoryForm


class categoryUpdateView(generic.UpdateView):
    model = models.category
    form_class = forms.categoryForm
    pk_url_kwarg = "pk"


class productListView(generic.ListView):
    model = models.product
    form_class = forms.productForm


class productCreateView(generic.CreateView):
    model = models.product
    form_class = forms.productForm


class productDetailView(generic.DetailView):
    model = models.product
    form_class = forms.productForm


class productUpdateView(generic.UpdateView):
    model = models.product
    form_class = forms.productForm
    pk_url_kwarg = "pk"


class brandListView(generic.ListView):
    model = models.brand
    form_class = forms.brandForm


class brandCreateView(generic.CreateView):
    model = models.brand
    form_class = forms.brandForm


class brandDetailView(generic.DetailView):
    model = models.brand
    form_class = forms.brandForm


class brandUpdateView(generic.UpdateView):
    model = models.brand
    form_class = forms.brandForm
    pk_url_kwarg = "pk"
