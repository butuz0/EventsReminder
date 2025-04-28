from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Event, RecurringEvent


class RecurringEventInline(admin.StackedInline):
    model = RecurringEvent
    extra = 0
    verbose_name = _('Recurring Event')
    verbose_name_plural = _('Recurring Events')
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (_('Recurrence Rule'), {'fields': ['recurrence_rule', 'recurrence_end_datetime']}),
        (_('Dates'), {'fields': ['created_at', 'updated_at']}),
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    def assigned_users(self, obj: Event) -> str:
        return ', '.join([user.get_full_name() or user.email for user in obj.assigned_to.all()])
    assigned_users.short_description = _('Assigned To')

    list_display = ['id', 'title', 'created_by', 'start_datetime', 'is_recurring', 'assigned_users']
    list_display_links = ['id', 'title']
    list_filter = ['is_recurring', 'priority', 'start_datetime']
    search_fields = ['title', 'description']
    autocomplete_fields = ['created_by', 'assigned_to']
    readonly_fields = ['created_by', 'created_at', 'updated_at']
    inlines = [RecurringEventInline]

    fieldsets = (
        (_('Basic Info'), {'fields': ['title', 'description', 'image', 'tags']}),
        (_('Time'), {'fields': ['start_datetime']}),
        (_('Participants'), {'fields': ['created_by', 'assigned_to']}),
        (_('Details'), {'fields': ['location', 'link', 'priority', 'is_recurring']}),
        (_('Dates'), {'fields': ['created_at', 'updated_at']})
    )


@admin.register(RecurringEvent)
class RecurringEventAdmin(admin.ModelAdmin):
    list_display = ['id', 'event', 'recurrence_rule', 'recurrence_end_datetime']
    list_display_links = ['id', 'event']
    readonly_fields = ['event', 'created_at', 'updated_at']

    fieldsets = (
        (_('Event'), {'fields': ['event']}),
        (_('Recurring Rule'), {'fields': ['recurrence_rule', 'recurrence_end_datetime']}),
        (_('Dates'), {'fields': ['created_at', 'updated_at']}),
    )
