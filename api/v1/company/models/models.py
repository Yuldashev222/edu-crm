from email.policy import default
from django.db import models

from api.v1.company.models.tariff import (
    Tariff,
)
# Create your models here.

class Petition(models.Model):
    flf = models.CharField(max_length=50)
    c_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    is_approved = models.BooleanField(default=False)
    company = models.ForeignKey('Company', on_delete=models.PROTECT, blank=True, null=True)
    def __str__(self):
        return f"{self.flf} {self.c_name}: {self.phone_number} - {self.is_approved}"
    
    

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True,
                                help_text='Company name must be unique.',
    )
    tariff = models.ForeignKey(Tariff, on_delete=models.PROTECT, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="uploads/companies/", null=True, blank=True)
    balance = models.FloatField(default=0)
    email = models.EmailField(null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    domain_name = models.CharField(
        max_length=30, unique=True, 
        help_text='Your domain will be "https://<Your domein>.maxsoft.uz/"',
        null=True, blank=True
    )
    stir = models.CharField(max_length=100, null=True, blank=True)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    bank_account_number = models.CharField(max_length=255, null=True, blank=True)
    main_target = models.TextField(null=True, blank=True)
    zip_code = models.CharField(max_length=30, null=True, blank=True)
    mfo = models.CharField(max_length=100, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    # is_branch = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    in_branch = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
    
    
    def save(self, *args, **kwargs):
        if self.name != self.name.lower():
            self.name = self.name.lower()
        if self.domain_name != self.domain_name.lower():
            self.domain_name = self.domain_name.lower()
        super().save(*args, **kwargs)


    def __str__(self):
        if self.email:
            return f"{self.name}: {self.email}"
        return f"{self.name}"
