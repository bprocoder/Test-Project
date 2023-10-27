from django.urls import path
from .views import *

urlpatterns = [
    path('user/', user, name='user'),
    path('user/sent/', send_mail, name='send_mail'),
]