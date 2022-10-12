
def upload_location_file(instance, file):
    """
    Faylga joylashgan address | format: (media)/company/tasks/creators/
    """
    return f'{instance.company}/tasks/{instance.task.creator}/{file}'
