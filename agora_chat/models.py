from django.db import models
from django.db.models import Q, UniqueConstraint
from mainapp.models import *
from django.urls import reverse


class chat_user(models.Model):
    chatuserid = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='user',to_field='id', blank=True, null=True)
    channel = models.TextField()
    orderid = models.ForeignKey(
        Orders, models.DO_NOTHING, db_column='orderid',to_field='ordersid')
    channel_status = models.BooleanField(default=False)
    RM = models.BooleanField(default=False)
    last_activity = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
    def __str__(self):
        return str(self.user.username)+"||||"+str(self.orderid)
    
class message(models.Model):
    messageid = models.AutoField(primary_key=True)
    channel = models.CharField(max_length=250)
    sender = models.CharField(max_length=200, null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    recieve_status = models.BooleanField(default=False)
    def __str__(self):
        return self.channel
    
# class fileHndler(models.Model):
#     name = models.CharField(max_length=200)
#     file = models.FileField(upload_to='uploads/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)
    
#     def get_absolute_url(self):
#         return reverse("download_file", kwargs={str(self.id)})
    
    # def __str__(self):
    #     return self.id

class single_chat(models.Model):
    user = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='user',to_field='id', blank=True, null=True)
    channel = models.TextField()
    channel_status = models.BooleanField(default=False)
    last_activity = models.DateTimeField(auto_now_add=True)
    channel_for_RM_chat = models.BooleanField(default=False)

    def __str__(self):
        return (self.channel)