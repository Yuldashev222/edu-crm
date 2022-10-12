from django.db import models


class Tariff(models.Model):
    price = models.FloatField(default=0)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.name} - {self.price}"
    