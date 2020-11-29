# Django
# Standard Library
from typing import Type, TypeVar

from django.core.exceptions import FieldDoesNotExist, ObjectDoesNotExist
from django.db import models, transaction
from django.urls import reverse
from django.utils.translation import gettext as _

# Third Party
import openfoodfacts
from django_fsm import FSMField
from googletrans import Translator
from django_oso.models import AuthorizedModel


T = TypeVar("T")


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


class Stock(AuthorizedModel):
    STATE_IN_STOCK = 'In Stock'
    STATE_CONSUMED = 'Consumed'
    STATE_TRANSFERRED = 'Transferred'
    STATE_REMOVED = 'Removed'

    STATES = [
        STATE_IN_STOCK,
        STATE_CONSUMED,
        STATE_TRANSFERRED,
        STATE_REMOVED,
    ]

    TEMPERATURE_ROOM_TEMPERATURE = 'Room Temperature'
    TEMPERATURE_CHILLED = 'Chilled'
    TEMPERATURE_FROZEN = 'Frozen'

    TEMPERATURES = [
        (TEMPERATURE_ROOM_TEMPERATURE, _(TEMPERATURE_ROOM_TEMPERATURE)),
        (TEMPERATURE_CHILLED, _(TEMPERATURE_CHILLED)),
        (TEMPERATURE_FROZEN, _(TEMPERATURE_FROZEN)),
    ]

    # Relationships
    location = models.ForeignKey("food.Location", on_delete=models.CASCADE)
    unit_of_measure = models.ForeignKey("food.UnitOfMeasure", on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey("food.Product", on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='stocks', on_delete=models.CASCADE)

    # Fields
    added = models.DateTimeField(auto_now_add=True)
    state = FSMField(_('State'), default=STATE_IN_STOCK, choices=list(zip(STATES, STATES)), protected=True)
    temperature = models.CharField(max_length=50, default=TEMPERATURE_ROOM_TEMPERATURE, choices=TEMPERATURES, blank=True)
    expires = models.DateField(blank=True, null=True)
    quantity = models.FloatField(blank=True, default=1)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return f'{self.product} - {self.quantity}'

    def get_absolute_url(self):
        return reverse("food_Stock_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("food_Stock_update", args=(self.pk,))

    def transfer(self, location, quantity=None):
        if self.location == location:
            raise Exception('Can not move to the same location')

        if not location.can_move_to:
            raise Exception('Can not move to this location')

        if quantity is None:
            quantity = self.quantity

        if quantity > self.quantity:
            raise Exception('Can not move more than you have')


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
    unit_of_measure = models.ForeignKey("food.UnitOfMeasure", on_delete=models.CASCADE, null=True, blank=True, default=None)

    # Fields
    name = models.CharField(max_length=50)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    code = models.CharField(max_length=30, unique=True)
    quantity = models.FloatField(blank=True, null=True, default=None)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("food_Product_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("food_Product_update", args=(self.pk,))

    @classmethod
    def get_or_lookup(cls: Type[T], code: str) -> T:
        try:
            return cls.objects.get(code=code)
        except ObjectDoesNotExist:
            return cls.lookup(code)

    @classmethod
    def lookup(cls, code):
        try:
            product = openfoodfacts.products.get_product(code)['product']
        except KeyError:
            raise ObjectDoesNotExist(f'{code} not found')

        name = None
        for key in ['generic_name', 'product_name']:
            try:
                name = product[key]
            except KeyError:
                pass

        try:
            categories = product['categories'].split(',')
        except KeyError:
            categories = []

        try:
            lang = product['categories_lc']
        except KeyError:
            lang = 'en'

        if lang != 'en':
            try:
                translator = Translator()
                categories = [c.text for c in translator.translate(categories, src=product['categories_lc'], dest='en')]
            except BaseException:
                categories = []

        if name is None:
            raise FieldDoesNotExist('Name not found')

        brand = product['brands']
        categories = filter(None, categories)

        try:
            quantity = product['product_quantity']
            unit_of_measure = f"{product['quantity']}".replace(f"{product['product_quantity']}", '')
        except KeyError:
            quantity = None
            unit_of_measure = None

        return cls.get_or_create(code, name, brand, categories, quantity, unit_of_measure)

    @classmethod
    def get_or_create(cls, code, name, brandName, categories, quantity=None, unit_of_measure=None):
        brandObject = Brand.objects.get_or_create(name=brandName.split(',')[0])[0]
        if isinstance(categories, str):
            categories.split(',')
        categoryObjects = [Category.objects.get_or_create(name=name)[0] for name in categories]

        if unit_of_measure is not None:
            unit_of_measure = UnitOfMeasure.objects.get_or_create(unit_of_measure)[0]

        defaults = {
            'name': name,
            'brand': brandObject,
            'quantity': quantity,
            'unit_of_measure': unit_of_measure,
        }
        prod = cls.objects.get_or_create(code=code, defaults=defaults)[0]
        prod.categories.set(categoryObjects)

        for key in defaults.keys():
            if getattr(prod, key) is None:
                setattr(prod, key, defaults[key])
        prod.save()

        return prod

    @transaction.atomic
    def transfer_in(self, quantity=1, expires=None, location=None):
        if location is None:
            location = Location.get_default()

        stock = Stock(product=self, quantity=quantity, expires=expires, location=location)
        stock.save()
        Transfer(destination=stock).save()

        return stock


class Transfer(AuthorizedModel):
    origin = models.ForeignKey("food.Stock", on_delete=models.CASCADE, null=True, blank=True, related_name='transferred_to')
    destination = models.ForeignKey("food.Stock", on_delete=models.CASCADE, related_name='transferred_from')
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    owner = models.ForeignKey('auth.User', related_name='transfers', on_delete=models.CASCADE)

    class Meta:
        pass

    def __str__(self) -> str:
        return f'{self.origin} to {self.destination}'.strip()


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
    TEMPERATURES = Stock.TEMPERATURES

    # Fields
    temperature = models.CharField(max_length=30, choices=TEMPERATURES)
    name = models.CharField(max_length=30)
    can_move_to = models.BooleanField(default=True)
    default = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def save(self, *args, **kwargs):
        if not self.default:
            return super().save(*args, **kwargs)
        with transaction.atomic():
            Location.objects.filter(default=True).update(default=False)
            return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("food_Location_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("food_Location_update", args=(self.pk,))

    @classmethod
    def get_default(cls):
        return cls.objects.filter(default=True).get()
