from django.db import models
import datetime

def get_current_date():
    return datetime.datetime.now().date()

# Create your models here.
class DolarPrice(models.Model):
    price = models.FloatField(default=0, blank=True)
    date_registered = models.DateField(default=get_current_date, blank=True)

    def __str__(self):
        return f"{self.price} {self.date_registered}"