# Standard Library
from collections import defaultdict
from dataclasses import dataclass, field
from functools import partialmethod

# Third Party
from django_fsm import FSMField as BaseFSMField
from django_fsm import get_all_FIELD_transitions


@dataclass(slots=True)
class State:
    name: str | None = None
    sources: set[str] = field(default_factory=set)
    destination: set[str] = field(default_factory=set)
    transitions_to: set[str] = field(default_factory=set)
    transitions_from: set[str] = field(default_factory=set)


def get_all_field_states(instance, field):
    states = defaultdict(lambda: State())

    for t in get_all_FIELD_transitions(instance, field):
        states[t.target].name = t.target
        states[t.source].name = t.source

        states[t.target].sources.add(t.source)
        states[t.target].transitions_to.add(t.name)

        states[t.source].destination.add(t.target)
        states[t.source].transitions_from.add(t.name)

    return states


class FSMField(BaseFSMField):
    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)

        setattr(cls, f"get_all_{self.name}_states", partialmethod(get_all_field_states, field=self))
