from django.db import models

# from api.v1.accounts.models import User
from api.v1.company.models.models import Company


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    language = models.CharField(max_length=15, unique=True)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class AbstractBaseMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
