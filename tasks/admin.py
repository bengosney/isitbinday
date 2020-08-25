from django.contrib import admin
from fsm_admin.mixins import FSMTransitionMixin


from .models import Task, Sprint


class TaskAdmin(FSMTransitionMixin, admin.ModelAdmin):
    list_display = ['title', 'effort', 'due_date', 'state', 'owner']
    readonly_fields = ['state', 'created', 'last_updated']
    fsm_field = ['state']


class SprintAdmin(FSMTransitionMixin, admin.ModelAdmin):
    list_display = ['title', 'state', 'owner']
    readonly_fields = ['state', 'started', 'finished', 'created', 'last_updated']
    fsm_field = ['state']


admin.site.register(Task, TaskAdmin)
admin.site.register(Sprint, SprintAdmin)
