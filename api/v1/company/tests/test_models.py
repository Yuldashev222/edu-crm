from api.v1.company.models.models import Company
from django.test import TestCase

class CompanyTestCase(TestCase):
    def test_Company(self):
        company = Company.objects.create(name='MaxSoft')
        print(company)
        self.assertEquals(str(company),'maxsoft')

