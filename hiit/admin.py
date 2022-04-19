import imp
from django.contrib import admin

from .models import Exercise, Workout

class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag_list', 'updated_at', 'created_at')
    search_fields = ('name', 'description')
    

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag_list', 'created_at', 'updated_at')
    search_fields = ('name', 'description')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Workout, WorkoutAdmin)