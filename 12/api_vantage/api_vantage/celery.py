from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_vantage.settings')

app = Celery('api_vantage')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическая загрузка задач из всех зарегистрированных Django-приложений.
app.autodiscover_tasks()
