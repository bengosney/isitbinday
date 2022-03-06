# Standard Library

# Django
from django.test import TestCase

# First Party
from food.models import Location


class LocationTestCase(TestCase):
    def test_default_location(self):
        location, _ = Location.objects.get_or_create(name="Kitchen", default=True)
        retrieved = Location.get_default()

        self.assertEqual(location, retrieved)
