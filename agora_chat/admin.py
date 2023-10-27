from django.contrib import admin
from .models import *

admin.site.register(chat_user)

admin.site.register(message)

admin.site.register(single_chat)