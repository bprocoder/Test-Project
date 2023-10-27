from django.db import models
from mainapp.models import *
from django.db.models import JSONField
# Create your models here.

class Appliedcandidates(models.Model):
    appliedcandidateid = models.AutoField(primary_key=True)
    firstname = models.TextField(blank=True, null=True)
    lastname = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    phone = models.BigIntegerField(blank=True, null=True)
    file = models.FileField(upload_to='appliedresume/',)
    creationdate = models.DateField(auto_now=True)
    jobhiringid = models.ForeignKey(
        Jobhiring, models.DO_NOTHING, blank=True, null=True)
    
class UserReferral(models.Model):
    user = models.OneToOneField(
        Allusers, models.DO_NOTHING, db_column='userid', blank=True, null=True)
    referral_id = models.CharField(max_length=100, default="12345")
    successful_referral_count = models.IntegerField(default=0)
    potential_referral_count = models.IntegerField(default=0)
    
    potential_referral_count_detail = JSONField(default=dict)
    
    # pass
    id = models.BigAutoField(primary_key=True)  # Specify BigAutoField as the primary key field

    # def __str__(self):
    #     return ' | '+self.user.username+' | '+self.referral_id+' | '+str(self.successful_referral_count)+' | '
    




class UTMDetails(models.Model):
    utm_source = models.CharField(max_length=100,default='other',null=True, blank=True)
    utm_medium = models.CharField(max_length=100,default='other',null=True, blank=True)
    utm_campaign = models.CharField(max_length=100,default='other',null=True, blank=True)
    utm_reference = models.CharField(max_length=100,default='None',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # pass
    id = models.BigAutoField(primary_key=True)  # Specify BigAutoField as the primary key field

    def __str__(self):
        return ' | '+str(self.utm_source)+' | '+str(self.utm_medium)+' | '+str(self.utm_campaign)+' | '+str(self.created_at)+' | '
