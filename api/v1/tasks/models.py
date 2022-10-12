from email.policy import default
from random import choices
from django.db import models
from api.v1.company.models.models import Company
from api.v1.general.enums import ProfileRoles, Sections, TaskStatuses
from api.v1.general.models import AbstractBaseMixin
from api.v1.accounts.models import User
from api.v1.tasks.services import upload_location_file
from mptt.fields import TreeForeignKey

# Create your models here.


class AbstractBaseTask(AbstractBaseMixin, models.Model):
    about = models.CharField(max_length=500, blank=True, null=True)
    text = models.TextField()
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    is_pinned = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=TaskStatuses.choices(), default=TaskStatuses.new.value)

    class Meta:
        abstract = True

class Task(AbstractBaseTask):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    parent = TreeForeignKey("self", models.CASCADE, related_name="children", null=True, blank=True)


class TaskItem(AbstractBaseTask):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    for_member = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    for_company = models.BooleanField(default=False)
    for_section = models.CharField(max_length=10, choices=Sections.choices(), blank=True, null=True)
    for_role = models.CharField(max_length=13, choices=ProfileRoles.choices(), blank=True, null=True)
    is_viewed = models.BooleanField(default=False)

class TaskUpload(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)
    task_item = models.ForeignKey(TaskItem, on_delete=models.CASCADE, blank=True, null=True)
    task_file = models.FileField(upload_to=upload_location_file)
    


