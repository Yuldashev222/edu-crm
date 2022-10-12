from django.db import models


from api.v1.accounts.models import (
    GroupUser,
)
from api.v1.company.models.models import (
    Company
)
from api.v1.education.models.mixins import (
    WeeksMixin
)
from api.v1.general.enums import Day
from api.v1.general.models import AbstractBaseMixin




# Rooms Model
class Rooms(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, blank=True, null=True)
    number_room = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}: {self.number_room}"


# Groups Model
class ClassGroups(AbstractBaseMixin, WeeksMixin, models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    room = models.ForeignKey(Rooms, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    start_date = models.DateField(help_text='Start group date')
    end_date = models.DateField(help_text='End group date')
    

    def __str__(self):
        return f"{self.name} - {self.teacher.first_name}"
    


class GroupTime(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    classGoup = models.ForeignKey('ClassGroups', on_delete=models.CASCADE)
    weekDay = models.CharField(max_length=9, choices=Day.choices())
    from_time = models.TimeField()
    to_time = models.TimeField()
    
    def __str__(self):
        return f"{self.classGoup.name} - {self.weekDay}: {self.from_time} - {self.to_time}"


class GroupMember(AbstractBaseMixin, models.Model):
    class_group = models.ForeignKey(ClassGroups, on_delete=models.PROTECT)
    member = models.ForeignKey(GroupUser, on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.class_group.name} - {self.member}"




