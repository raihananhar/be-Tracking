from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Load settings dari Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover task di apps Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
