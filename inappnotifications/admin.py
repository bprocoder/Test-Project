from django.contrib import admin
from .models import *
from .models import notification

class NotificationAdmin(admin.ModelAdmin):
    list_display=('__str__','timestamp')

    ordering = ['-timestamp']

admin.site.register(notification, NotificationAdmin)

admin.site.register([clientnotification,influencernotification,RMnotification,managernotification,accountsnotification,KYCnotification,BrandOrAgencynotification,AdminNotification,EmailTemplate,TelegramNotification])
