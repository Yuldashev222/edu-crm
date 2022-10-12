import datetime
from django.db import models



from api.v1.accounts.models import (
    GroupUser,
    Mentor,
    Teacher,
    Student
)
from api.v1.education.models.class_group import (
    ClassGroups
)
from api.v1.general.models import AbstractBaseMixin


class Lesson(AbstractBaseMixin, models.Model):
    # teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    class_group = models.ForeignKey(ClassGroups, on_delete=models.PROTECT)
    theme = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.class_group.name}: {self.theme}"
    


# Attendance in every lesson group
class Attendance(AbstractBaseMixin, models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)
    student = models.ForeignKey(GroupUser, on_delete=models.PROTECT)
    is_came = models.BooleanField(default=False)
    is_reasonable = models.BooleanField(default=False)
    reason = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f"{self.class_group.name}"
    

class HomeWork(AbstractBaseMixin, models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    author = models.ForeignKey(GroupUser, on_delete=models.SET_NULL, null=True)
    