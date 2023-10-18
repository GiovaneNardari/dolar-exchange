from django.db import models

# Create your models here.
class DolarPrice(models.Model):
    value = models.FloatField()
    date_time = models.DateTimeField()

    def __str__(self):
        return f"{self.value} {self.date_time}"