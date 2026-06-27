import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jurassic_blog.settings')
app = Celery('jurassic_blog')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()