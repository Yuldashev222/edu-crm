from email.policy import default
from django.db import models
from api.v1.education.services import upload_location_image, validate_size_image
from api.v1.general.enums import Regions
from phonenumber_field import modelfields
from django.core.validators import FileExtensionValidator

from api.v1.company.models.models import (
    Company,
)
from api.v1.education.models.class_group import (
    ClassGroups,
    Rooms,
)
from api.v1.education.models.courses import (
    Courses,
)
from api.v1.general.models import (
    AbstractBaseMixin
)
from api.v1.accounts.models import (
    Student,
    User
)


# Exams for entry 
class Exam(AbstractBaseMixin, models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Courses, on_delete=models.PROTECT)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_entry = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    def __str__(self):
        return f"{self.company.name}: {self.course.name}"
    

class ExamStudent(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(verbose_name='Name', max_length=50)
    last_name = models.CharField(verbose_name='Surname', max_length=50)
    phone_number = modelfields.PhoneNumberField()
    region_1 = models.CharField(max_length=15, choices=Regions.choices(), help_text='province of birth')
    
    def save(self, *args, **kwargs):
        self.first_name = self.student.first_name
        self.last_name = self.student.last_name
        self.phone_number = self.student.phone_number
        self.region_1 = self.student.region_1
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.phone_number}: {self.exam.course.name}"
    

class ExamUploads(models.Model):
    question = models.ForeignKey('ExamQuestion', on_delete=models.CASCADE, blank=True, null=True)
    answer = models.ForeignKey('ExamQuestionVariant', on_delete=models.CASCADE, blank=True, null=True)
    # File uchun validatsiya
    exam_file = models.FileField(
        upload_to=upload_location_image,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg', 'svg']), validate_size_image],
    )

    def __str__(self):
        return f'{self.exam_file}'



class ExamQuestion(AbstractBaseMixin, models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.PROTECT)
    text = models.TextField()
    q_file = models.FileField(upload_to='exam/questions/files', blank=True, null=True)
    is_open = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.exam.course.name}"

class ExamQuestionVariant(AbstractBaseMixin, models.Model):
    question = models.ForeignKey('ExamQuestion', on_delete=models.PROTECT)
    text = models.CharField(max_length=1000)
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.id}: {self.is_true}"


class ExamQuestionAnswer(AbstractBaseMixin, models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey('ExamQuestion', on_delete=models.PROTECT)
    variant = models.ForeignKey('ExamQuestionVariant', on_delete=models.SET_NULL, null=True, blank=True)
    text = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f"{self.student.first_name}: {self.student.phone_number}"
