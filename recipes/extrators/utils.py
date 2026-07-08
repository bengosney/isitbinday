# Standard Library
import fractions
from datetime import timedelta
from functools import lru_cache
from unicodedata import normalize

# Third Party
import requests


def un_unicode(string: str) -> str:
    out = ""
    for char in string:
        normalized = normalize("NFKC", char).replace("⁄", "/")

        if normalized != char:
            normalized = str(float(fractions.Fraction(normalized)))[1:]
        out += normalized

    return out


def get_isosplit(s, split):
    if split in s:
        n, s = s.split(split)
    else:
        n = 0
    return n, s


def parse_isoduration(s: str) -> timedelta:
    try:
        s = s.split("P")[-1]
    except IndexError, AttributeError:
        return timedelta()

    days, s = get_isosplit(s, "D")
    _, s = get_isosplit(s, "T")
    hours, s = get_isosplit(s, "H")
    minutes, s = get_isosplit(s, "M")
    seconds, s = get_isosplit(s, "S")

    return timedelta(days=int(days), hours=int(hours), minutes=int(minutes), seconds=int(seconds))


@lru_cache
def get_raw_html(url: str) -> str:
    r = requests.get(url)
    return r.text
