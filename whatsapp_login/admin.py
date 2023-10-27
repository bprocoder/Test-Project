from django.contrib import admin
from .models import *



class WhatsappuserAdmin(admin.ModelAdmin):
    # Fields to search in the search bar
    search_fields = ['clientid__username', 'access_id', 'secret_id']

    # Displayed columns in the list view
    list_display = ['clientid', 'access_id', 'secret_id']
    
    

admin.site.register(UsedJWToken)

admin.site.register(Whatsappuser, WhatsappuserAdmin)

admin.site.register(ShortURL)