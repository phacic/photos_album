from django.db.models.signals import (post_save)
from django.db.models.base import ModelBase
from django.dispatch import receiver

from .models import Photo, Album
from config.utils import AuditVerbEnum

from audit.tasks import task_log_audit


@receiver(signal=post_save, sender=Photo)
def handle_photo_save(sender: ModelBase, instance: Photo, **kwargs):
    """ log photo changes in audit """

    label = instance._meta.app_label
    model = instance._meta.model_name
    verb = AuditVerbEnum.CREATED.value if kwargs.get('created') else AuditVerbEnum.UPDATED.value

    # since images and album are created by users it is safe to
    # assume the user created and updated them
    user_id = instance.user_id

    task_log_audit.apply_async(args=(user_id, verb, label, model, instance.id))


@receiver(signal=post_save, sender=Album)
def handle_album_save(sender, instance: Album, **kwargs):
    """ log album changes in audit """

    label = instance._meta.app_label
    model = instance._meta.model_name
    verb = AuditVerbEnum.CREATED.value if kwargs.get('created') else AuditVerbEnum.UPDATED.value

    # since images and album are created by users it is safe to
    # assume the user created and updated them
    user_id = instance.user_id

    task_log_audit.apply_async(args=(user_id, verb, label, model, instance.id))

