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

        context["state_tasks"] = tasks

        return context
