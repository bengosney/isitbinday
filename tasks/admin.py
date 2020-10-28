# Django
from django.contrib import admin

# Third Party
from adminsortable2.admin import SortableAdminMixin
from django_fsm_log.admin import StateLogInline
from fsm_admin.mixins import FSMTransitionMixin

# Locals
from .models import Sprint, Task


class TaskAdmin(SortableAdminMixin, FSMTransitionMixin, admin.ModelAdmin):
    list_display = ['title', 'effort', 'due_date', 'state', 'owner', 'completed']
    list_filter = ['state']
    readonly_fields = ['state', 'created', 'last_updated']
    fsm_field = ['state']
    inlines = [StateLogInline]

    def get_queryset(self, request):
        qs = self.model.admin_objects.get_queryset()

        ordering = self.ordering or ()
        if ordering:
            qs = qs.order_by(*ordering)

        return qs


class SprintAdmin(FSMTransitionMixin, admin.ModelAdmin):
    list_display = ['title', 'state', 'owner']
    readonly_fields = ['state', 'started', 'finished', 'created', 'last_updated']
    fsm_field = ['state']


admin.site.register(Task, TaskAdmin)
admin.site.register(Sprint, SprintAdmin)
