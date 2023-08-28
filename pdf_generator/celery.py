import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pdf_generator.settings')

app = Celery('pdf_generator')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


