from django.db import models

# Create your models here.
class TrafficSource(models.Model):
    utm_source = models.CharField(max_length=100, unique=True)
    count=models.IntegerField(default=0)