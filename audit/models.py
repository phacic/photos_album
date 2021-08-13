from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model

from config.utils import AuditVerbEnum


User = get_user_model()


class Audit(models.Model):
    # the user perform the action
    user = models.ForeignKey(User, related_name='audits', on_delete=models.CASCADE)
    # the action being performed (created, updated, deleted)
    action = models.CharField(max_length=2, choices=AuditVerbEnum.to_list())
    # content action was performed on
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-create_date']

    def __str__(self):
        return f'{self.action} on {self.content_object} id {self.object_id}'
