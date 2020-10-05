from django.contrib import admin
from fsm_admin.mixins import FSMTransitionMixin
from adminsortable2.admin import SortableAdminMixin


from .models import Task, Sprint


class TaskAdmin(SortableAdminMixin, FSMTransitionMixin, admin.ModelAdmin):
    list_display = ['title', 'effort', 'due_date', 'state', 'owner']
    readonly_fields = ['state', 'created', 'last_updated']
    fsm_field = ['state']

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
