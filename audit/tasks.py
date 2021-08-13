from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from celery import Task
from config.celery import app as celery_app
from config.utils import AuditVerbEnum, backoff

from .models import Audit

User = get_user_model()


@celery_app.task(name='audit.log_audit', bind=True, max_retries=3, ignore_result=True)
def task_log_audit(self: Task, user_id: int, verb: AuditVerbEnum, app_label: str, model: str, object_id: int):
    """ log changes into audit """

    try:
        # get object using content type
        obj_type = ContentType.objects.get(app_label=app_label, model=model)
        user = User.objects.get(id=user_id)

        # save audit
        Audit.objects.create(action=verb, user=user, content_type=obj_type, object_id=object_id)

    except Exception as ex:
        wait = backoff(self.request.retries)
        self.retry(countdown=wait, exc=ex)
