# Standard Library
import json
import re
from fractions import Fraction

# Django
from django.contrib.auth.models import User

# Third Party
from minestrone import HTML

# Locals
from ..models import Ingredient, Recipe, Step, Unit
from .utils import get_raw_html, parse_isoduration, un_unicode


class Yoast:
    def __init__(self, owner: User) -> None:
        self.owner = owner

    def parse(self, raw_json: str, url: str | None = None) -> int:
        data = json.loads(raw_json)
        recipe_node = None
        if "@graph" in data:
            for node in data["@graph"]:
                if node.get("@type", "").lower() == "recipe":
                    recipe_node = node
                    break
        if not recipe_node:
            return 0

        cook_time = parse_isoduration(recipe_node.get("cookTime", ""))
        prep_time = parse_isoduration(recipe_node.get("prepTime", ""))
        recipe, _ = Recipe.objects.update_or_create(
            owner=self.owner,
            name=recipe_node["name"],
            defaults={
                "description": recipe_node.get("description", ""),
                "time": cook_time + prep_time,
                "link": url or "",
            },
        )
        ingredient_regex = re.compile(r"^(([0-9\.\/]+)\s*([\w,\.]+))\s+(.+)$")
        default_unit, _ = Unit.objects.get_or_create(name="of")
        for ingredient in recipe_node.get("recipeIngredient", []):
            norm = un_unicode(ingredient)
            matches = ingredient_regex.match(norm)
            name = norm
            defaults = {"unit": default_unit, "quantity": 1}
            if matches:
                name = matches[4]
                if Unit.is_unit(matches[3]):
                    unit, _ = Unit.objects.get_or_create(name=matches[3])
                    defaults["unit"] = unit
                else:
                    name = f"{matches[3]} {name}"
                defaults["quantity"] = float(Fraction(matches[2]))
            Ingredient.objects.update_or_create(
                owner=self.owner,
                recipe=recipe,
                name=name,
                defaults=defaults,
            )
        for instruction in recipe_node.get("recipeInstructions", []):
            text = instruction["text"] if isinstance(instruction, dict) else instruction
            Step.objects.get_or_create(
                owner=self.owner,
                recipe=recipe,
                description=text,
            )
        return 1

    def extract(self, url: str) -> int:
        raw_html = HTML(get_raw_html(url))
        for e in raw_html.query('script[type="application/ld+json"]'):
            try:
                data = json.loads(e.text or "")
                if "@graph" in data:
                    return self.parse(json.dumps(data), url)
            except Exception:
                continue
        return 0
