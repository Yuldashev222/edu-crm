from unicodedata import name
from django.db import models

from api.v1.accounts.models import (
    Mentor,
    Teacher,
    Student
)
from api.v1.company.models.models import (
    Company
)
from api.v1.education.models.courses import (
    Courses
)
from api.v1.education.models.lessons import (
    Attendance,
    # AttendanceStudent,
    Lesson,
    # LessonTask,
    # TaskItems
)
from api.v1.education.models.mixins import (
    WeeksMixin
)
from api.v1.education.models.class_group import (
    ClassGroups,
    Rooms,
    # TeachersInGroup
)


# Courses Model
class CoursesHistory(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.name


# Rooms Model
class RoomsHistory(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, blank=True, null=True)
    number_room = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}: {self.number_room}"


# Groups Model
class ClassGroupsHistory(WeeksMixin, models.Model):
    class_group = models.ForeignKey(ClassGroups, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    room = models.ForeignKey(Rooms, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    from_time = models.TimeField()
    to_time = models.TimeField()
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False)
    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.teacher.first_name}"
    
    @property
    def get_room(self):
        pass
    


class LessonHistory(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    class_group = models.ForeignKey(ClassGroups, on_delete=models.PROTECT)
    theme = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False)
    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.class_group.name}: {self.theme}"
    
    

# Attendance in every lesson group
class AttendanceHistory(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.PROTECT)
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)
    current_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False)
    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.class_group.name}"

