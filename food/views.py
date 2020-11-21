# Django
from django.views import generic

# Third Party
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# First Party
from food.serializers import LookupSerializer

# Locals
from . import forms, models


@api_view(['GET'])
def LookupProduct(request, code):
    serializer = LookupSerializer(data={'code': code})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnitOfMeasureListView(generic.ListView):
    model = models.UnitOfMeasure
    form_class = forms.UnitOfMeasureForm


class UnitOfMeasureCreateView(generic.CreateView):
    model = models.UnitOfMeasure
    form_class = forms.UnitOfMeasureForm


class UnitOfMeasureDetailView(generic.DetailView):
    model = models.UnitOfMeasure
    form_class = forms.UnitOfMeasureForm


class UnitOfMeasureUpdateView(generic.UpdateView):
    model = models.UnitOfMeasure
    form_class = forms.UnitOfMeasureForm
    pk_url_kwarg = "pk"


class StockListView(generic.ListView):
    model = models.Stock
    form_class = forms.StockForm


class StockCreateView(generic.CreateView):
    model = models.Stock
    form_class = forms.StockForm


class StockDetailView(generic.DetailView):
    model = models.Stock
    form_class = forms.StockForm


class StockUpdateView(generic.UpdateView):
    model = models.Stock
    form_class = forms.StockForm
    pk_url_kwarg = "pk"


class CategoryListView(generic.ListView):
    model = models.Category
    form_class = forms.CategoryForm


class CategoryCreateView(generic.CreateView):
    model = models.Category
    form_class = forms.CategoryForm


class CategoryDetailView(generic.DetailView):
    model = models.Category
    form_class = forms.CategoryForm


class CategoryUpdateView(generic.UpdateView):
    model = models.Category
    form_class = forms.CategoryForm
    pk_url_kwarg = "pk"


class ProductListView(generic.ListView):
    model = models.Product
    form_class = forms.ProductForm


class ProductCreateView(generic.CreateView):
    model = models.Product
    form_class = forms.ProductForm


class ProductDetailView(generic.DetailView):
    model = models.Product
    form_class = forms.ProductForm


class ProductUpdateView(generic.UpdateView):
    model = models.Product
    form_class = forms.ProductForm
    pk_url_kwarg = "pk"


class BrandListView(generic.ListView):
    model = models.Brand
    form_class = forms.BrandForm


class BrandCreateView(generic.CreateView):
    model = models.Brand
    form_class = forms.BrandForm


class BrandDetailView(generic.DetailView):
    model = models.Brand
    form_class = forms.BrandForm


class BrandUpdateView(generic.UpdateView):
    model = models.Brand
    form_class = forms.BrandForm
    pk_url_kwarg = "pk"


class LocationListView(generic.ListView):
    model = models.Location
    form_class = forms.LocationForm


class LocationCreateView(generic.CreateView):
    model = models.Location
    form_class = forms.LocationForm


class LocationDetailView(generic.DetailView):
    model = models.Location
    form_class = forms.LocationForm


class LocationUpdateView(generic.UpdateView):
    model = models.Location
    form_class = forms.LocationForm
    pk_url_kwarg = "pk"
