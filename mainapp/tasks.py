# from celery.decorators import task
from celery.utils.log import get_task_logger
from celery import shared_task
import time
import requests
from .models import ExchangeRates
import traceback
from datetime import datetime
from .backgroundfunctions import *
logger = get_task_logger(__name__)
from inappnotifications.views import send_message
# msg1=msg.replace('.', '\.').replace('-', '\-').replace('!', '\!')

@shared_task
def errortesting_task():
    try:
        errortesting()

    except Exception as e:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('my_task_errors.log', 'a') as f:
            f.write(f'{now}: {traceback.format_exc()}')
        print(f'errortesting Error: {str(e)}')
        send_message(1241208476, f'{now}: {traceback.format_exc()}')
        
        

@shared_task
def videoslotpushnotification_task():
    try:
        videoslotpushnotification()
    except Exception as e:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('my_task_errors.log', 'a') as f:
            f.write(f'{now}: {traceback.format_exc()}')
        print(f'Error: {str(e)}')
        send_message(1241208476, f'{now}: {traceback.format_exc()}')


@shared_task
def monitoranupdateorderstatus_task():
    try:
        monitoranupdateorderstatus()
        # print('>>>>>>>>>>>>>>>>>>>>>>>>>HERE>>>>>>>>>>>>>>>>>')
    except Exception as e:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('my_task_errors.log', 'a') as f:
            f.write(f'{now}: {traceback.format_exc()}')
        print(f'Error: {str(e)}')
        send_message(1241208476, f'{now}: {traceback.format_exc()}')

@shared_task
def monitoranusenddelaywarning_task():
    try:
        monitoranusenddelaywarning()
    except Exception as e:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('my_task_errors.log', 'a') as f:
            f.write(f'{now}: {traceback.format_exc()}')
        print(f'Error: {str(e)}')
        send_message(1241208476, f'{now}: {traceback.format_exc()}')

@shared_task
def topcreator1_task():
    try:
        topcreator1()
    except Exception as e:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('my_task_errors.log', 'a') as f:
            f.write(f'{now}: {traceback.format_exc()}')
        print(f'Error: {str(e)}')
        send_message(1241208476, f'{now}: {traceback.format_exc()}')






























# @shared_task
# def start_convertrates():
#     while True:
#         print(111)
#         url = 'https://v6.exchangerate-api.com/v6/34875784293d57a535d18367/latest/INR'
#         response = requests.get(url=url).json()
#         # print("gdfgsdf", response['conversion_rates'])
#         for x in response['conversion_rates'].keys():
#             # print(x, " => ", response['conversion_rates'][x])
#             ex = ExchangeRates.objects.filter(countery_abbrevation=x)
#             if ex.exists():
#                 ex = ex[0]
#                 ex.rates = response['conversion_rates'][x]
#                 ex.save(update_fields=['rates'])
#                 # print("upadtes rates")
#             else:
#                 ex = ExchangeRates(countery_abbrevation=x,
#                                    rates=response['conversion_rates'][x])
#                 ex.save()
#                 print("Fucntion execute")
#         time.sleep(5)

