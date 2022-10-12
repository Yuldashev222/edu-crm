from django.contrib import admin

from api.v1.company.models.models import (
    Company,
)
from api.v1.company.models.history import (
    HistoryCompany
)
from api.v1.company.models.tariff import (
    Tariff
)
# Register your models here.


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", 'email')
    

@admin.register(HistoryCompany)
class HistoryCompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", 'email')

@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ("id", "name", 'price')