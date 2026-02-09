# Third Party
import pytest

# Locals
from ..extrators import Yoast
from ..models import Recipe

SAMPLE_YOAST_JSON = """
{
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "Recipe",
         "name": "Brunede Kartofler (Danish Caramelized Potatoes)",
         "author": {"@id": "https://www.example.com/#/schema/person/c70639949ef702685a6dfd260dae11ac"},
         "description": "Buttery potatoes browned in caramelized sugar, Brunede Kartofler are a popular and traditional Danish side dish enjoyed especially at Christmastime.",
         "datePublished": "2023-07-25T08:55:43+00:00",
         "image": [
             "https://www.example.com/wp-content/uploads/2021/12/photo.jpg"
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


@pytest.mark.django_db
class TestYoastExtractor:
    def test_parse_yoast_recipe(self, user, unit_of):
        extractor = Yoast(user)
        count = extractor.parse(SAMPLE_YOAST_JSON, url="https://www.example.com/brunede-kartofler/")
        assert count == 1

        recipe = Recipe.objects.get(name="Brunede Kartofler (Danish Caramelized Potatoes)")
        assert recipe.description == (
            "Buttery potatoes browned in caramelized sugar, Brunede Kartofler are a popular "
            "and traditional Danish side dish enjoyed especially at Christmastime."
        )
        assert recipe.ingredients.count() == 3
        assert recipe.steps.count() == 2

        ingredients = [i.name for i in recipe.ingredients.all()]
        assert "firm, waxy potatoes  (, choose small ones that are uniform in size)" in ingredients
        assert "granulated sugar" in ingredients[1]
        assert "butter" in ingredients[2]

        steps = [s.description for s in recipe.steps.all()]
        assert any("Boil the potatoes" in s for s in steps)
        assert any("Place the sugar" in s for s in steps)

    def test_parse_yoast_recipe_without_url(self, user, unit_of):
        extractor = Yoast(user)
        count = extractor.parse(SAMPLE_YOAST_JSON)
        assert count == 1

        recipe = Recipe.objects.get(name="Brunede Kartofler (Danish Caramelized Potatoes)")
        assert recipe.link == ""
