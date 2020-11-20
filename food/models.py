from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


class UnitOfMeasure(models.Model):

    # Fields
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("food_UnitOfMeasure_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("food_UnitOfMeasure_update", args=(self.pk,))


class Stock(models.Model):

    # Relationships
    location = models.ForeignKey("food.Location", on_delete=models.CASCADE)
    unit_of_measure = models.ForeignKey("food.UnitOfMeasure", on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey("food.Product", on_delete=models.CASCADE)

    # Fields
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    added = models.DateTimeField(auto_now_add=True)
    quantity = models.FloatField()
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("food_Stock_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("food_Stock_update", args=(self.pk,))


class Category(models.Model):

    # Fields
    name = models.CharField(max_length=50)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("food_Category_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("food_Category_update", args=(self.pk,))


class Product(models.Model):

    # Relationships
    categories = models.ManyToManyField("food.Category")
    brand = models.ForeignKey("food.Brand", on_delete=models.CASCADE)

    # Fields
    name = models.CharField(max_length=50)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    code = models.CharField(max_length=30)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("food_Product_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("food_Product_update", args=(self.pk,))

    @classmethod
    def get_or_create(cls, code, name, brandName, categories):
        brandObject = Brand.objects.get_or_create(name=brandName.split(',')[0])[0]
        categoryObjects = [Category.objects.get_or_create(name=name)[0] for name in categories.split(',')]
 
        prod = cls.objects.get_or_create(code=code, defaults={
            'name': name,
            'brand': brandObject,
        })[0]
        prod.categories.set(categoryObjects)
        return prod


class Brand(models.Model):

    # Fields
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("food_Brand_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("food_Brand_update", args=(self.pk,))


class Location(models.Model):

    TYPE_ROOM = 'Room Temperature'
    TYPE_FRIDGE = 'Fridge'
    TYPE_FREEZER = 'Freezer'

    TYPES = [
        (TYPE_ROOM, _(TYPE_ROOM)),
        (TYPE_FRIDGE, _(TYPE_FRIDGE)),
        (TYPE_FREEZER, _(TYPE_FREEZER)),
    ]

    # Fields
    type = models.CharField(max_length=30, choices=TYPES)
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("food_Location_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("food_Location_update", args=(self.pk,))
