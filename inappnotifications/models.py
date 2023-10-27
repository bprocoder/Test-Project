from django.db import models
from mainapp.models import * 

class notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    user = models.ForeignKey(
        Allusers, models.DO_NOTHING, db_column='user', to_field='id', blank=True, null=True)
    read = models.BooleanField(default=False)
    slotnotisendstatus = models.BooleanField(default=False)
    redirect_link = models.TextField()
    icon = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)

class clientnotification(models.Model):
    name = models.TextField()
    head = models.CharField(max_length=255)
    body = models.TextField()
    redirect_link = models.TextField()
    icon = models.TextField()
    
    def __str__(self):
        return str(self.name)

class influencernotification(models.Model):
    name = models.TextField()
    head = models.CharField(max_length=255)
    body = models.TextField()
    redirect_link = models.TextField()
    icon = models.TextField()
    
    def __str__(self):
        return str(self.name)

class RMnotification(models.Model):
    name = models.TextField()
    head = models.CharField(max_length=255)
    body = models.TextField()
    redirect_link = models.TextField()
    icon = models.TextField()
    
    def __str__(self):
        return str(self.name)

class managernotification(models.Model):
    name = models.TextField()
    head = models.CharField(max_length=255)
    body = models.TextField()
    redirect_link = models.TextField()
    icon = models.TextField()
    
    def __str__(self):
        return str(self.name)

class accountsnotification(models.Model):
    name = models.TextField()
    head = models.CharField(max_length=255)
    body = models.TextField()
    redirect_link = models.TextField()
    icon = models.TextField()
    
    def __str__(self):
        return str(self.name)

class KYCnotification(models.Model):
    name = models.TextField()
    head = models.CharField(max_length=255)
    body = models.TextField()
    redirect_link = models.TextField()
    icon = models.TextField()
    
    def __str__(self):
        return str(self.name)

class BrandOrAgencynotification(models.Model):
    name = models.TextField()
    head = models.CharField(max_length=255)
    body = models.TextField()
    redirect_link = models.TextField()
    icon = models.TextField()
    
    def __str__(self):
        return str(self.name)

class AdminNotification(models.Model):
    name = models.TextField()
    head = models.CharField(max_length=255)
    body = models.TextField()
    redirect_link = models.TextField()
    icon = models.TextField()
    
    def __str__(self):
        return str(self.name)


class EmailTemplate(models.Model):
    template_id = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    html_content = models.TextField()  # store the HTML content directly or a path to the HTML file

    def __str__(self):
        return str(self.template_id)

class TelegramNotification(models.Model):
    chat_id = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.user_id)
