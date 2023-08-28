import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pdf_generator.settings')

app = Celery('pdf_generator')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete_read_tasks_every_one_hour': {
        'task': 'notes.tasks.remove_reports',
        'schedule': 3600,
        'options': {
            'expires': 50
        }
    }
}
