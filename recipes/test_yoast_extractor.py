# Django
from django.contrib.auth.models import User
from django.test import TestCase

# Locals
from .extrators import YoastExtractor
from .models import Recipe, Unit

SAMPLE_YOAST_JSON = """
{
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "Recipe",
         "name": "Brunede Kartofler (Danish Caramelized Potatoes)",
         "author": {"@id": "https://www.daringgourmet.com/#/schema/person/c70659949ef702685a6dfd260dae11ac"},
         "description": "Buttery potatoes browned in caramelized sugar, Brunede Kartofler are a popular and traditional Danish side dish enjoyed especially at Christmastime.",
         "datePublished": "2023-07-25T08:55:43+00:00",
         "image": [
             "https://www.daringgourmet.com/wp-content/uploads/2021/12/Brunede-Kartofler-3.jpg"
         ],
         "recipeYield": ["4"],
         "prepTime": "PT20M",
         "cookTime": "PT15M",
         "totalTime": "PT515M",
         "recipeIngredient": [
             "2 pounds firm, waxy potatoes  (, choose small ones that are uniform in size)",
             "1/4 cup granulated sugar",
             "2 tablespoons butter"
         ],
         "recipeInstructions": [
             {"@type": "HowToStep", "text": "Boil the potatoes in salted water with their skins on until done, being careful not to over-cook.  Once cool enough to handle but still warm (it makes peeling easier), remove the skins (this takes time and patience).  Put the potatoes in the fridge to thoroughly chill for several hours.  Ideally they should be chilled overnight."},
             {"@type": "HowToStep", "text": "Place the sugar in a heavy cast iron skillet over medium heat and allow it to melt, stirring as infrequently as possible to prevent burning. The sugar will melt and begin to brown.  Let it come to a rich golden brown color.  Add the butter and stir while allowing it to melt.   Once the butter is melted and incorporated into the sugar, add the cold potatoes.  Stir to thoroughly coat all of them.  Don&#39;t worry if the sugar starts to crystalize, it will melt again. Let the potatoes cook, stirring only occasionally to re-coat them in the sugar glaze, until they&#39;re lightly browned.  (How much you brown them is a matter of personal preference, but I like to have some of those glorious browned crusted bits on the potatoes.)"}
         ]
        }
    ]
}
"""


class YoastExtractorTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        Unit.objects.get_or_create(name="of")

    def test_parse_yoast_recipe(self):
        extractor = YoastExtractor(self.user)
        count = extractor.parse(SAMPLE_YOAST_JSON)
        self.assertEqual(count, 1)
        recipe = Recipe.objects.get(name="Brunede Kartofler (Danish Caramelized Potatoes)")
        self.assertEqual(
            recipe.description,
            "Buttery potatoes browned in caramelized sugar, Brunede Kartofler are a popular and traditional Danish side dish enjoyed especially at Christmastime.",
        )
        self.assertEqual(recipe.ingredients.count(), 3)
        self.assertEqual(recipe.steps.count(), 2)
        ingredients = [i.name for i in recipe.ingredients.all()]
        self.assertIn("firm, waxy potatoes  (, choose small ones that are uniform in size)", ingredients)
        self.assertIn("granulated sugar", ingredients[1])
        self.assertIn("butter", ingredients[2])
        steps = [s.description for s in recipe.steps.all()]
        self.assertTrue(any("Boil the potatoes" in s for s in steps))
        self.assertTrue(any("Place the sugar" in s for s in steps))
