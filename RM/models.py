from django.db import models
from mainapp.models import * 

# Create your models here.
class RMsReview(models.Model):
    rmsreviewid = models.AutoField(primary_key=True)
    clientid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='clientid', to_field='id')
    rmid = models.ForeignKey(Rmsettings, models.DO_NOTHING, db_column='rmid', to_field='rmid')
    review_message = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=1)
    isapproved = models.BooleanField(default=False)
    approveuserid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='approveuserid', to_field='id', blank=True, null=True, related_name='approveid')
    date = models.DateTimeField(auto_now=True)

