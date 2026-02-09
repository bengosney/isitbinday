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


class SchemaOrg:
    def __init__(self, owner: User) -> None:
        self.owner = owner

    def parse(self, raw_html: str, url: str | None = None) -> int:
        ingredient_regex = re.compile(r"^(([\d\.\/]+)\s*([\w,\.]+))\s+(.+)$")
        default_unit, _ = Unit.objects.get_or_create(name="of")

        html = HTML(raw_html)
        found = 0
        for e in html.query('script[type="application/ld+json"]'):
            data = json.loads(e.text or "")

            if "@type" not in data or f"{data['@type']}".lower() != "recipe":
                continue

            found += 1
            cook_time = parse_isoduration(data.get("cookTime", 0))
            prep_time = parse_isoduration(data.get("prepTime", 0))

            recipe, _ = Recipe.objects.update_or_create(
                owner=self.owner,
                name=data["name"],
                defaults={
                    "description": data["description"],
                    "time": cook_time + prep_time,
                    "link": url,
                },
            )

            for ingredient in data["recipeIngredient"]:
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

                ingredient, _ = Ingredient.objects.update_or_create(
                    owner=self.owner,
                    recipe=recipe,
                    name=name,
                    defaults=defaults,
                )

            for instruction in data["recipeInstructions"]:
                Step.objects.get_or_create(
                    owner=self.owner,
                    recipe=recipe,
                    description=instruction["text"],
                )

        return found

    def extract(self, url: str) -> int:
        raw_html = get_raw_html(url)
        return self.parse("".join(raw_html), url)
