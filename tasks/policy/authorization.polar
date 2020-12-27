 
# Task Rule

allow(actor, "retrieve", task: tasks::Task) if
    task.owner = actor;

allow(actor, "update", task: tasks::Task) if
    task.owner = actor;

allow(actor, "do", task: tasks::Task) if 
    task.owner = actor;

allow(actor, "done", task: tasks::Task) if 
    task.owner = actor;

allow(actor, "archive", task: tasks::Task) if 
    task.owner = actor;

allow(actor, "cancel", task: tasks::Task) if 
    task.owner = actor;

allow(actor, "retrieve", sprint: tasks::Sprint) if
    sprint.owner = actor;