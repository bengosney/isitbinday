# Third Party
from vanilla import ListView

# Locals
from .models import Task


class TaskListView(ListView):
    model = Task
