from email.policy import default
from unicodedata import name
from django.db import models

from api.v1.company.models.models import (
    Company,
)
from api.v1.general.models import AbstractBaseMixin


# Courses Model
class Courses(AbstractBaseMixin, models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    duration_in_month = models.FloatField(default=0, help_text="Kurs davomiyligi oyda.")
    
    def __str__(self):
        return self.name
