from datetime import datetime

from django.db import models
from django.utils.translation import gettext as _
from django_fsm import FSMField, transition


class StateMixin():
    @property
    def available_state_transitions(self):
        return [i.name for i in self.get_available_state_transitions()]


class Task(StateMixin, models.Model):
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
    due_date = models.DateField(_('Due Date'), blank=True, null=True, default=None)
    effort = models.IntegerField(_('Effort'), default=0)
    blocked_by = models.ForeignKey('Task', related_name='blocks', on_delete=models.SET_NULL, null=True, blank=True)

    owner = models.ForeignKey('auth.User', related_name='tasks', on_delete=models.CASCADE)

    state = FSMField(_('State'), default=STATE_TODO, choices=list(zip(STATES, STATES)), protected=True)

    created = models.DateTimeField(_('Created'), auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(_('Last Updated'), auto_now=True, editable=False)

    def __str__(self):
        return f'{self.title}'

    @transition(field=state, source=STATE_DRAFT, target=STATE_TODO)
    def todo(self):
        pass

    @transition(field=state, source=STATE_TODO, target=STATE_DOING)
    def do(self):
        pass

    @transition(field=state, source=[STATE_TODO, STATE_DOING], target=STATE_DONE)
    def done(self):
        pass

    @transition(field=state, source=[STATE_DRAFT, STATE_TODO, STATE_DOING], target=STATE_CANCELED)
    def cancel(self):
        pass


class Sprint(StateMixin, models.Model):
    STATE_PLANNING = 'planning'
    STATE_IN_PROGRESS = 'in progress'
    STATE_FINISHED = 'finished'
    STATE_CANCELED = 'canceled'

    STATES = [
        STATE_PLANNING,
        STATE_IN_PROGRESS,
        STATE_FINISHED,
        STATE_CANCELED,
    ]

    title = models.CharField(_('Title'), max_length=255)

    state = FSMField(_('State'), default=STATE_PLANNING, choices=list(zip(STATES, STATES)), protected=True)
    started = models.DateTimeField(_('Started'), editable=False, null=True, blank=True)
    finished = models.DateTimeField(_('Finished'), editable=False, null=True, blank=True)

    tasks = models.ManyToManyField(Task)

    owner = models.ForeignKey('auth.User', related_name='sprints', on_delete=models.CASCADE)

    created = models.DateTimeField(_('Created'), auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(_('Last Updated'), auto_now=True, editable=False)

    @transition(field=state, source=STATE_PLANNING, target=STATE_IN_PROGRESS)
    def start(self):
        self.started = datetime.now()

    @transition(field=state, source=STATE_IN_PROGRESS, target=STATE_FINISHED)
    def finish(self):
        self.finished = datetime.now()

    @transition(field=state, source=STATE_PLANNING, target=STATE_CANCELED)
    def cancel(self):
        pass