from __future__ import absolute_import, unicode_literals

import os

from django.conf import settings
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "config.settings")

app = Celery('config')
app.config_from_object('config.celeryconfig')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True, name="root.debug_task")
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
