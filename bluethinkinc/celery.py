from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings module for 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bluethinkinc.settings')

# Create Celery app instance
app = Celery('bluethinkinc')

# Load settings from Django settings file, using CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks in installed apps
app.autodiscover_tasks()

# Define Celery Beat schedule for periodic tasks
app.conf.beat_schedule = {
    'check-login-at-10am': {
        'task': 'bluethinkapp.tasks.check_login_and_notify',  # Task path
        'schedule': crontab(hour=10, minute=0),  # Schedule for 10 AM daily
    },
}
