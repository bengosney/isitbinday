# Standard Library
import fractions
import json
import re
from datetime import timedelta
from unicodedata import normalize

# Django
from django.contrib.auth.models import User

# Third Party
import requests
from minestrone import HTML

# Locals
from .file_cache import file_cache
from .models import Ingredient, Recipe, Step, Unit


class schema_org:
    @staticmethod
    def un_unicode(string: str) -> str:
        out = ""
        for char in string:
            normalized = normalize("NFKC", char).replace("⁄", "/")

            if normalized != char:
                normalized = str(float(fractions.Fraction(normalized)))[1:]
            out += normalized

        return out

    @staticmethod
    def get_isosplit(s, split):
        if split in s:
            n, s = s.split(split)
        else:
            n = 0
        return n, s

    @classmethod
    def parse_isoduration(cls, s):

        # Remove prefix
        s = s.split("P")[-1]

        # Step through letter dividers
        days, s = cls.get_isosplit(s, "D")
        _, s = cls.get_isosplit(s, "T")
        hours, s = cls.get_isosplit(s, "H")
        minutes, s = cls.get_isosplit(s, "M")
        seconds, s = cls.get_isosplit(s, "S")

        # Convert all to seconds
        return timedelta(days=int(days), hours=int(hours), minutes=int(minutes), seconds=int(seconds))

    def extract(self, raw_html: str) -> None:
        ingredientRegex = re.compile(r"^(([\d\.]+)\s+(\w+))\s+(.+)$")
        owner = User.objects.get(id=1)

        html = HTML(raw_html)
        for e in html.query('script[type="application/ld+json"]'):
            data = json.loads(e.text or "")

            cook_time = self.parse_isoduration(data["cookTime"])
            prep_time = self.parse_isoduration(data["prepTime"])

            recipe, _ = Recipe.objects.get_or_create(
                owner=owner, name=data["name"], defaults={"description": data["description"], "time": cook_time + prep_time}
            )

            for ingredient in data["recipeIngredient"]:
                norm = self.un_unicode(ingredient)
                matches = ingredientRegex.match(norm)
                if matches:
                    unit, _ = Unit.objects.get_or_create(name=matches[3])
                    ingredient, _ = Ingredient.objects.get_or_create(
                        owner=owner, recipe=recipe, name=matches[4], defaults={"unit": unit, "quantity": float(matches[2])}
                    )

            instructions = [""] * len(data["recipeInstructions"])
            for ins in data["recipeInstructions"]:
                step = int(ins["name"].replace("Step ", ""))
                instructions[step - 1] = ins["text"]

            for instruction in instructions:
                step, _ = Step.objects.get_or_create(owner=owner, recipe=recipe, description=instruction)


@file_cache
def get_raw_html(url: str) -> str:
    r = requests.get(url)
    return r.text
