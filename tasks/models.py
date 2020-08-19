from django.db import models
from django.utils.translation import gettext as _
from django_fsm import FSMField, transition


class Task(models.Model):
    STATE_DRAFT = 'draft'
    STATE_TODO = 'todo'
    STATE_DOING = 'doing'
    STATE_DONE = 'done'
    STATE_CANCELED = 'canceled'

    STATES = [
        STATE_DRAFT,
        STATE_TODO,
        STATE_DOING,
        STATE_DONE,
        STATE_CANCELED
    ]

    title = models.CharField(_('Title'), max_length=255)
    due_date = models.DateTimeField(_('Due Date'), blank=True, null=True, default=None)
    effort = models.IntegerField(_('Effort'), default=0)

    state = FSMField(_('State'), default=STATE_TODO, choices=list(zip(STATES, STATES)), protected=True)

    created = models.DateTimeField(_('Created'), auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(_('Last Updated'), auto_now=True, editable=False)

    @transition(field=state, source=STATE_DRAFT, target=STATE_TODO)
    def todo(self):
        pass

    @transition(field=state, source=STATE_TODO, target=STATE_DOING)
    def do(self):
        pass

    @transition(field=state, source=STATE_DOING, target=STATE_DONE)
    def done(self):
        pass

    @transition(field=state, source=[STATE_DRAFT, STATE_TODO, STATE_DOING], target=STATE_CANCELED)
    def cancel(self):
        pass