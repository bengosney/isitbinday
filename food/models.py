from pprint import pprint
from django.db import models
from django.urls import reverse


class category(models.Model):

    # Fields
    name = models.CharField(max_length=50)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("food_category_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("food_category_update", args=(self.pk,))


class product(models.Model):
    # Fields
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=30)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    # Relationships
    categories = models.ManyToManyField("food.category")
    brand = models.ForeignKey("food.brand", on_delete=models.CASCADE)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("food_product_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("food_product_update", args=(self.pk,))

    @classmethod
    def get_or_create(cls, code, name, brandName, categories):
        brandObject = brand.objects.get_or_create(name=brandName.split(',')[0])[0]
        pprint(brandObject)
        categoryObjects = [category.objects.get_or_create(name=name)[0] for name in categories.split(',')]

        prod = cls.objects.get_or_create(code=code, defaults={
            'name': name,
            'brand': brandObject,
        })[0]

        prod.categories.set(categoryObjects)

        return prod


class brand(models.Model):

    # Fields
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("food_brand_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("food_brand_update", args=(self.pk,))
