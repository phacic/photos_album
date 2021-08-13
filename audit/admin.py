from django.contrib import admin
from .models import Audit


class AuditAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'action']


admin.site.register(Audit, AuditAdmin)
