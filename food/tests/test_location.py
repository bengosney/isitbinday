# Third Party
import pytest

# Locals
from ..models import Location


@pytest.mark.django_db
def test_default_location():
    location, _ = Location.objects.get_or_create(name="Kitchen", default=True)
    retrieved = Location.get_default()

    assert location == retrieved
