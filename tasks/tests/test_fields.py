# Third Party
import pytest

# Locals
from ..fields import State


@pytest.mark.django_db
def test_all_states(task):
    states = task.get_all_state_states()

    example = State(
        name="todo",
        sources={"doing", "draft"},
        destination={"done", "canceled", "doing"},
        transitions_to={"todo"},
        transitions_from={"done", "cancel", "do"},
    )

    assert states["todo"] == example
