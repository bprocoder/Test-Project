from django.db import models
from mainapp.models import *
# Create your models here.


class Orderdefaultquestions(models.Model):
    defualtquestionid = models.AutoField(primary_key=True)
    question = models.TextField(blank=True, null=True)
    subheading = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    serviceid = models.ForeignKey(
        Services, models.DO_NOTHING, db_column='serviceid', to_field='serviceid', blank=True, null=True)


class Influencerquestions(models.Model):
    influencerquestionsid = models.AutoField(primary_key=True)
    influencerid = models.ForeignKey(InfluencerProfile, models.DO_NOTHING,
                                     db_column='influencerid', to_field='influencer_userid', blank=True, null=True)
    # This field type is a guess.
    serviceid = models.ForeignKey(
        Services, models.DO_NOTHING, db_column='serviceid', to_field='serviceid', blank=True, null=True)
    question = models.TextField(blank=True, null=True)
    subheading = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)



class Defaultreviews(models.Model):
    defaultreviewsid = models.AutoField(primary_key=True)
    serviceid = models.ForeignKey(
        Services, models.DO_NOTHING, db_column='serviceid', to_field='serviceid', blank=True, null=True)
    reviews = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)





class Orderrequirementquestions(models.Model):
    orderrequirementquestionsid = models.AutoField(primary_key=True)
    answer = models.TextField(blank=True, null=True)
    question = models.ForeignKey(
        Influencerquestions, models.DO_NOTHING, db_column='question', to_field='influencerquestionsid')
    orderid = models.ForeignKey(
        Orders, models.DO_NOTHING, db_column='orderid', to_field='ordersid')
    date = models.DateTimeField(auto_now_add=True)
