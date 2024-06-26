# Standard Library
from datetime import datetime

# Django
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext as _

# Third Party
from django_fsm import FSMField, transition
from django_fsm_log.models import StateLog
from django_oso.models import AuthorizedModel
from recurrent.event_parser import RecurringEvent


class StateMixin:
    @property
    def available_state_transitions(self):
        return [i.name for i in self.get_available_state_transitions()]


class Task(StateMixin, AuthorizedModel):
    class Meta:
        ordering = ["position"]

    STATE_DRAFT = "draft"
    STATE_TODO = "todo"
    STATE_DOING = "doing"
    STATE_DONE = "done"
    STATE_CANCELED = "canceled"
    STATE_ARCHIVE = "archive"

    STATES = [
        STATE_TODO,
        STATE_DOING,
        STATE_DONE,
        STATE_CANCELED,
        STATE_ARCHIVE,
    ]

    STATES_DUE_DATE_MATTERS = [
        STATE_TODO,
        STATE_DOING,
    ]

    HIDDEN_STATES = [STATE_ARCHIVE]

    title = models.CharField(_("Title"), max_length=255)
    due_date = models.DateField(_("Due Date"), blank=True, null=True, default=None)
    show_after = models.DateField(_("Show After"), default=timezone.now)
    effort = models.IntegerField(_("Effort"), default=0)
    blocked_by = models.ForeignKey("Task", related_name="blocks", on_delete=models.SET_NULL, null=True, blank=True)
    completed = models.DateTimeField(_("Completed on"), blank=True, null=True)
    repeats = models.CharField(_("Repeats"), max_length=255, blank=True, default="")

    owner = models.ForeignKey("auth.User", related_name="tasks", on_delete=models.CASCADE)

    state = FSMField(
        _("State"),
        default=STATE_TODO,
        choices=list(zip(STATES, STATES)),
        protected=True,
    )

    position = models.PositiveIntegerField(default=0, blank=False, null=False)
    created = models.DateTimeField(_("Created"), auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(_("Last Updated"), auto_now=True, editable=False)

    @classmethod
    def auto_archive(cls, before):
        tasks = cls.objects.filter((Q(state=cls.STATE_DONE) | Q(state=cls.STATE_CANCELED)) & Q(completed__lte=before))

        for task in tasks:
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

    @transition(field=state, source=[STATE_DRAFT, STATE_DOING], target=STATE_TODO)
    def todo(self):
        pass

    @transition(field=state, source=STATE_TODO, target=STATE_DOING)
    def do(self):
        pass

    @transition(field=state, source=[STATE_TODO, STATE_DOING], target=STATE_DONE)
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
        source=[STATE_DRAFT, STATE_TODO, STATE_DOING],
        target=STATE_CANCELED,
    )
    def cancel(self):
        pass

    @transition(field=state, source=[STATE_DONE, STATE_CANCELED], target=STATE_ARCHIVE)
    def archive(self):
        pass

    def __str__(self):
        return f"{self.title}"


class Sprint(StateMixin, AuthorizedModel):
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
    )
    started = models.DateTimeField(_("Started"), editable=False, null=True, blank=True)
    finished = models.DateTimeField(_("Finished"), editable=False, null=True, blank=True)

    tasks = models.ManyToManyField(Task)

    owner = models.ForeignKey("auth.User", related_name="sprints", on_delete=models.CASCADE)

    created = models.DateTimeField(_("Created"), auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(_("Last Updated"), auto_now=True, editable=False)

    @transition(field=state, source=STATE_PLANNING, target=STATE_IN_PROGRESS)
    def start(self):
        self.started = datetime.now()

    @transition(field=state, source=STATE_IN_PROGRESS, target=STATE_FINISHED)
    def finish(self):
        self.finished = datetime.now()

    @transition(field=state, source=STATE_PLANNING, target=STATE_CANCELED)
    def cancel(self):
        pass

    def __str__(self):
        return f"{self.title}"
