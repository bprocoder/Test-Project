from django.db import models
from mainapp.models import *

class zoomeet(models.Model):
    orderid = models.ForeignKey(
        Orders, models.DO_NOTHING, db_column='orderid',to_field='ordersid')
    meet_link = models.TextField()
    meet_id = models.TextField()
    meet_password = models.TextField()
    schedule_date = models.DateTimeField(auto_now_add=True)
    
    ismeetingend=models.BooleanField(default=False)
    islinksent=models.BooleanField(default=False)
    
    
    
    def __str__(self):
        return str(self.orderid)

class zoomtoken(models.Model):
    access_token = models.TextField()
    refresh_token = models.TextField()
