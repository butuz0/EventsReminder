from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('event', 'notification_method', 'notification_datetime', 'is_sent')
    list_filter = ('notification_method', 'is_sent')
    search_fields = ('event__title', 'notification_method')
    ordering = ('-notification_datetime',)
    date_hierarchy = 'notification_datetime'
    list_per_page = 20
    readonly_fields = ('event', 'created_by', 'celery_task_id', 'is_sent')
    
    fieldsets = (
        (None, {
            'fields': ('event', 'notification_method', 'notification_datetime', 'celery_task_id', 'is_sent')
        }),
    )
