# Django
from django.test import TestCase

# Locals
from .models import Tag


class testTag(TestCase):
    def test_new(self):
        title = "new tag"
        newTag = Tag.getTag(title)

        self.assertEqual(f"{newTag}", title)

    def test_existing(self):
        title = "new tag 2"
        newTag = Tag.getTag(title)
        newTag.save()

        existingTag = Tag.getTag(title)

        self.assertEqual(newTag.pk, existingTag.pk)
        self.assertIsNotNone(existingTag.pk)
