from django.db import models

# Create your models here.
class DolarPrices(models.Model):
    price = models.FloatField()
    updated_at = models.DateTimeField()