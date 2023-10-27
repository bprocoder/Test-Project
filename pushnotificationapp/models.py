from django.db import models
from mainapp.models import *

class fcmuserandbrowerid(models.Model):
    user = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='user', to_field='id', blank=True, null=True)
    browserid = models.TextField()
    
    def _str_(self):
        return str(self.user.username)


class SendNotificationtoUser(models.Model):
    userid = models.TextField()
    title = models.TextField()
    body = models.TextField()
    
    def __str__(self):
        return(self.userid)