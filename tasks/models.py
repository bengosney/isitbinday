# Standard Library
from contextlib import suppress
from datetime import datetime

# Django
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext as _

# Third Party
from django_fsm import FSMField, TransitionNotAllowed, transition
from django_fsm_log.models import StateLog
from recurrent.event_parser import RecurringEvent

# First Party
from utils import SaveContextManagerMixin


class OwnerManager(models.Manager):
    def for_user(self, user):
        """Return a queryset filtered by the owner."""
        return self.filter(owner=user)


class StateMixin:
    def get_available_state_transitions(self):
        raise NotImplementedError("Subclasses must implement get_available_state_transitions()")

    @property
    def available_state_transitions(self):
        return [i.name for i in self.get_available_state_transitions()]


class Task(StateMixin, models.Model, SaveContextManagerMixin):
    ARCHIVE_STATE_ACTIVE = "active"
    ARCHIVE_STATE_ARCHIVED = "archived"
    ARCHIVE_STATES = [
        ARCHIVE_STATE_ACTIVE,
        ARCHIVE_STATE_ARCHIVED,
    ]

    STATE_DRAFT = "draft"
    STATE_TODO = "todo"
    STATE_DOING = "doing"
    STATE_DONE = "done"
    STATE_CANCELED = "canceled"

    STATES = [
        STATE_TODO,
        STATE_DOING,
        STATE_DONE,
        STATE_CANCELED,
    ]

    STATES_DUE_DATE_MATTERS = [
        STATE_TODO,
        STATE_DOING,
    ]

    HIDDEN_STATES = []

    title = models.CharField(_("Title"), max_length=255)
    due_date = models.DateField(_("Due Date"), blank=True, null=True, default=None)
    show_after = models.DateField(_("Show After"), default=timezone.now)
    effort = models.IntegerField(_("Effort"), default=0)
    blocked_by = models.ForeignKey("Task", related_name="blocks", on_delete=models.SET_NULL, null=True, blank=True)
    completed = models.DateTimeField(_("Completed on"), blank=True, null=True)
    repeats = models.CharField(_("Repeats"), max_length=255, blank=True, default="")

    archived = FSMField(
        _("Archived"),
        default=ARCHIVE_STATE_ACTIVE,
        choices=list(zip(ARCHIVE_STATES, ARCHIVE_STATES)),
        protected=True,
    )  # type: ignore

    owner = models.ForeignKey("auth.User", related_name="tasks", on_delete=models.CASCADE)

    state = FSMField(
        _("State"),
        default=STATE_TODO,
        choices=list(zip(STATES, STATES)),
        protected=True,
    )  # type: ignore

    position = models.PositiveIntegerField(default=0, blank=False, null=False)
    created = models.DateTimeField(_("Created"), auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(_("Last Updated"), auto_now=True, editable=False)

    objects = OwnerManager()

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return f"{self.title}"

    @classmethod
    def auto_archive(cls, before):
        tasks = cls.objects.filter((Q(state=cls.STATE_DONE) | Q(state=cls.STATE_CANCELED)) & Q(completed__lte=before))

        for task in tasks:
            with suppress(TransitionNotAllowed):
                task.archive()
                task.save()

        return len(tasks)

    @property
    def previous_state(self):
        type_id = ContentType.objects.get_for_model(self)
        state_log = StateLog.objects.all().filter(object_id=self.pk, content_type_id=type_id).order_by("-timestamp")

        try:
            return state_log[0].source_state
        except IndexError:
            return None

    @transition(field=state, source=[STATE_DRAFT, STATE_DOING], target=STATE_TODO)  # type: ignore
    def todo(self):
        pass

    @transition(field=state, source=STATE_TODO, target=STATE_DOING)
    def do(self):
        pass

    @transition(field=state, source=[STATE_TODO, STATE_DOING], target=STATE_DONE)  # type: ignore
    def done(self):
        self.completed = timezone.make_aware(datetime.now())

        if self.repeats != "":
            next = self.__class__(
                title=self.title,
                effort=self.effort,
                owner=self.owner,
                repeats=self.repeats,
            )
            r = RecurringEvent(now_date=self.completed)
            next.show_after = r.parse(f"in {self.repeats}")

            next.save()

    @transition(
        field=state,
        source=[STATE_DRAFT, STATE_TODO, STATE_DOING],  # type: ignore
        target=STATE_CANCELED,
    )
    def cancel(self):
        pass

    @transition(
        field=archived,
        source=ARCHIVE_STATE_ACTIVE,
        target=ARCHIVE_STATE_ARCHIVED,
        conditions=[lambda self: self.state in [self.STATE_DONE, self.STATE_CANCELED]],
    )  # type: ignore
    def archive(self):
        pass


class Sprint(StateMixin, models.Model):
    STATE_PLANNING = "planning"
    STATE_IN_PROGRESS = "in progress"
    STATE_FINISHED = "finished"
    STATE_CANCELED = "canceled"

    STATES = [
        STATE_PLANNING,
        STATE_IN_PROGRESS,
        STATE_FINISHED,
        STATE_CANCELED,
    ]

    title = models.CharField(_("Title"), max_length=255)

    state = FSMField(
        _("State"),
        default=STATE_PLANNING,
        choices=list(zip(STATES, STATES)),
        protected=True,
    )  # type: ignore
    started = models.DateTimeField(_("Started"), editable=False, null=True, blank=True)
    finished = models.DateTimeField(_("Finished"), editable=False, null=True, blank=True)

    tasks = models.ManyToManyField(Task)

    owner = models.ForeignKey("auth.User", related_name="sprints", on_delete=models.CASCADE)

    created = models.DateTimeField(_("Created"), auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(_("Last Updated"), auto_now=True, editable=False)

    objects = OwnerManager()

    def __str__(self):
        return f"{self.title}"

    @transition(field=state, source=STATE_PLANNING, target=STATE_IN_PROGRESS)
    def start(self):
        self.started = datetime.now()

    @transition(field=state, source=STATE_IN_PROGRESS, target=STATE_FINISHED)
    def finish(self):
        self.finished = datetime.now()

    @transition(field=state, source=STATE_PLANNING, target=STATE_CANCELED)
    def cancel(self):
        pass
