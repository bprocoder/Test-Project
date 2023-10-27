from django.db import models
from mainapp.models import *
import string
import random


class UsedJWToken(models.Model):
    token_id = models.TextField(unique=True)  # Store the unique identifier
    status=models.BooleanField(default=False)

    def __str__(self):
        return self.token_id
    
    
class Whatsappuser(models.Model):
    clientid = models.OneToOneField(
        Allusers,on_delete=models.CASCADE, db_column='clientid', to_field='username')
    access_id = models.TextField()  # Store the unique identifier
    secret_id = models.TextField()  # Store the unique identifier

    def __str__(self):
        return str(self.clientid)


class ShortURL(models.Model):
    long_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True)

    def save(self, *args, **kwargs):
        self.short_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        super().save(*args, **kwargs)
