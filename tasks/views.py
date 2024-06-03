# Django
from django.http import HttpResponse

# Third Party
from vanilla import ListView

# Locals
from .models import Task


class TaskListView(ListView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks: dict[str, list[Task]] = {state: [] for state in Task.STATES if state != "archive"}

        for task in context["object_list"]:
            tasks[task.state].append(task)

        context["tasks_by_state"] = tasks

        return context


def action_view(request, id, action):
    return HttpResponse(f"Performed {action} on {id}")
