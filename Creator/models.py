from django.db import models
from mainapp.models import *
# Create your models here.



class DefaultManager(models.Model):
    defaultmanagerid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='userid', blank=True, null=True)
    
    
class Topinfluencer(models.Model):
    topinfluencerid = models.AutoField(primary_key=True)
    influencerid = models.OneToOneField(InfluencerSettings, models.DO_NOTHING,
                                     db_column='influencerid', to_field='influencer_userid')
    ordercompleteioncount=models.BigIntegerField(default=0)


class DefaultRM(models.Model):
    defaultrmid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='userid', blank=True, null=True)
    userassignedcount=models.BigIntegerField(default=0)
    
    


class Defaulttimezoneinfluencer(models.Model):
    defaulttimezoneinfluencerid = models.AutoField(primary_key=True)
    userid = models.OneToOneField(
        Allusers, models.DO_NOTHING, db_column='userid', blank=True, null=True)
    timezone = models.TextField(blank=True, null=True)
    
    


class ScheduleCompletionTasks(models.Model):
    schedulecompletiontaskid = models.AutoField(primary_key=True)
    date = models.DateTimeField(blank=True,null=True)
    orderid = models.ForeignKey(
        Orders, models.DO_NOTHING, db_column='orderid', blank=True, null=True)
    comptask=models.BooleanField(default=False)

    def __str__(self):
        return str(self.schedulecompletiontaskid)




class Webstoryfiles(models.Model):
    webstoryfilesid = models.AutoField(primary_key=True)
    webstoryfiles = models.FileField(upload_to='webstories/')


    def __str__(self):
        return str(self.webstoryfilesid)
    
class Webstory(models.Model):
    webstoryid = models.AutoField(primary_key=True)
    title = ArrayField(models.TextField(blank=True, null=True), default=list, blank=True, null=True)
    # Remove the storypath field from here
    filesid = ArrayField(models.IntegerField(blank=True, null=True), default=list, blank=True, null=True)
    caption = ArrayField(models.TextField(blank=True, null=True), default=list, blank=True, null=True)
    userid = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='userid', blank=True, null=True)
    date = models.DateTimeField(auto_now=True)
    thumbnail = models.FileField(upload_to='', blank=True, null=True)
    thumnailtitle = models.TextField(blank=True, null=True, unique=True)
    isapproved = models.BooleanField(default=False)
    aprovedby = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='aprovedby', blank=True, null=True, related_name='approvedby')

    def __str__(self):
        return str(self.webstoryid)




class InfluencerSeoSettings(models.Model):
    influencer_seo_settingsid = models.AutoField(primary_key=True)
    influencer_userid = models.OneToOneField(InfluencerProfile, models.DO_NOTHING,
                                             db_column='influencerid', to_field='influencer_userid', blank=True, null=True)
    title = models.TextField(blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    keyword = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.influencer_userid)


class OrderResponse(models.Model):
    orderresponseid = models.AutoField(primary_key=True)
    orderid = models.ForeignKey(
        Orders, models.DO_NOTHING, db_column='orderid', blank=True, null=True)
    videoid = models.ForeignKey(
        Videos, models.DO_NOTHING, db_column='videoid', blank=True, null=True)
    videolink = models.ForeignKey(
        VideosLink, models.DO_NOTHING, db_column='videolinkid', blank=True, null=True)
    ordersummary = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.orderresponseid)


class Whychooseselected(models.Model):
    whychooseselectedid = models.AutoField(primary_key=True)
    choosetext = ArrayField(models.TextField(
        blank=True, null=True), default=list, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    selectid=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.whychooseselectedid)


class Gigsselected(models.Model):
    gigsselectedid = models.AutoField(primary_key=True)
    gigtext = ArrayField(models.TextField(
        blank=True, null=True), default=list, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.gigsselectedid)


class Aboutselected(models.Model):
    aboutselectedid = models.AutoField(primary_key=True)
    abouttext = models.TextField(
        blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    selectid=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.aboutselectedid)
    
    
class Shortdesselected(models.Model):
    shortdesselectedid = models.AutoField(primary_key=True)
    shortdestext = models.TextField(
        blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    selectid=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.shortdesselectedid)

