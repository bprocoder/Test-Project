# django_celery/celery.py

import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
app = Celery("myproject")
app.config_from_object("django.conf:settings", namespace="CELERY")
#Celery Beat Settings
app.conf.beat_schedule = {
    # 'reset_allow_trading_for_the_day_task':{
    #     'task': 'clcp_rcbeatapp.tasks.reset_allow_trading_for_the_day_task',
    #     'schedule': crontab(minute = '*', hour= '*', day_of_week='*', day_of_month= '*', month_of_year= '*'),
    # },
    
    'get_recording_download_link_task':{

        'task': 'zoomeet.tasks.get_recording_download_link_task',
        'schedule': crontab(minute = '*', hour= '*', day_of_week='*', day_of_month= '*', month_of_year= '*'),
    },
    
    # 'errortesting_task':{
    #     'task': 'mainapp.tasks.errortesting_task',
    #     # 'schedule': crontab(),
    #     'schedule': crontab(minute = '*', hour= '*', day_of_week='*', day_of_month= '*', month_of_year= '*'),
    # },

    'notifyuserforvideochat_task':{
        'task': 'zoomeet.tasks.notifyuserforvideochat_task',
        'schedule': crontab(minute = '*', hour= '*', day_of_week='*', day_of_month= '*', month_of_year= '*'),
    },

    'compafterdays_task':{
        'task': 'Creator.tasks.compafterdays_task',
        'schedule': crontab(minute = '*', hour= '*', day_of_week='*', day_of_month= '*', month_of_year= '*'),
    },

    'send_task':{
        'task': 'pushnotificationapp.tasks.send_task',
        'schedule': crontab(minute = '*', hour= '*', day_of_week='*', day_of_month= '*', month_of_year= '*'),
    },
    
    'videoslotpushnotification_task':{
        'task': 'mainapp.tasks.videoslotpushnotification_task',
        # 'schedule': crontab(minute = '*', hour= '*', day_of_week='*', day_of_month= '*', month_of_year= '*'),
        'schedule': crontab(hour=12, minute=15, day_of_week='*'),
    },

    'monitoranupdateorderstatus_task':{
        'task': 'mainapp.tasks.monitoranupdateorderstatus_task',
        # 'schedule': crontab(),
        'schedule': crontab(hour=12, minute=15, day_of_week='*'),
    },

    'monitoranusenddelaywarning_task':{
        'task': 'mainapp.tasks.monitoranusenddelaywarning_task',
        # 'schedule': crontab(),
        'schedule': crontab(hour=12, minute=15, day_of_week='*'),
    },

    'topcreator1_task':{
        'task': 'mainapp.tasks.topcreator1_task',
        # 'schedule': crontab(),
        'schedule': crontab(hour=12, minute=15, day_of_week='*'),
    },

    
    # crontab(hour=7, minute=30, day_of_week=1),
    # crontab(minute=0, hour=0) Execute daily at midnight.
}
app.autodiscover_tasks()

# @app.task(bind=True)
# def debug_task(self):
#     print("app.tasKkkk, debug_task()")
#     print('Request: {0!r}'.format(self.request))
