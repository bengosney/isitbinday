 
# Task Rule

allow(actor, "view", task: tasks::Task) if
    task.owner != actor;