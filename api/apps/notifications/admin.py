from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'notification_method', 'notification_datetime', 'is_sent']
    list_filter = ['notification_method', 'is_sent']
    ordering = ['-notification_datetime']
    date_hierarchy = 'notification_datetime'
    list_per_page = 20
    readonly_fields = ['created_by', 'celery_task_id', 'is_sent']

    fieldsets = (
        ('Generic relation', {
            'fields': ('content_type', 'object_id')
        }),
        ('Notification data', {
            'fields': ('notification_method', 'notification_datetime', 'celery_task_id', 'is_sent')
        }),
    )
