from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models.base import ModelBase
from django.dispatch import receiver

from config.utils import AuditVerbEnum

from audit.tasks import task_log_audit

User = get_user_model()


@receiver(signal=post_save, sender=User)
def handle_user_save(sender, instance: AbstractUser, **kwargs):
    """ log user updates to audit """
    label = instance._meta.app_label
    model = instance._meta.model_name
    verb = AuditVerbEnum.CREATED.value if kwargs.get('created') else AuditVerbEnum.UPDATED.value

    # users create and update themselves
    user_id = instance.id

    task_log_audit.apply_async(args=(user_id, verb, label, model, instance.id))
