from rest_framework.test import APITestCase
from rest_framework import status


class CompanyAPITestCase(APITestCase):
    def create_company(self):
        print('s')
        data = {
            "name":"ilmziynati",
            "email":"ilmziynati@gmail.com",
        }
        print(data)
        response = self.client.post('api/v1/company/', data)
        self.assertEquals(response.statis_code, status.HTTP_201_CREATED)
        