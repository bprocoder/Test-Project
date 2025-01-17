# from celery.utils.log import get_task_logger
from celery import shared_task
from .views import get_recording_download_link, notifyuserforvideochat
from inappnotifications.views import send_message
# from celery.decorators import periodic_task
# from datetime import timedelta

# import time
# from threading import Thread
# # from .models import Test_Read_Write

# import logging
import traceback
from datetime import datetime
# logger = get_task_logger(__name__)
@shared_task#(bind=True)
def get_recording_download_link_task():#(self) cron task executed here to renew open order for the next day that have been cancelled due to market close
    
    try:
        get_recording_download_link()
    except Exception as e:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('my_task_errors.log', 'a') as f:
            f.write(f'{now}: {traceback.format_exc()}')
        print(f'Error: {str(e)}')
        send_message(1241208476, f'{now}: {traceback.format_exc()}')

@shared_task#(bind=True)
def notifyuserforvideochat_task():
    try:
        notifyuserforvideochat()
    except Exception as e:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('my_task_errors.log', 'a') as f:
            f.write(f'{now}: {traceback.format_exc()}')
        print(f'Error: {str(e)}')
        send_message(1241208476, f'{now}: {traceback.format_exc()}')

