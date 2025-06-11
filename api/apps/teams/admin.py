from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Team, Invitation


class InvitationInline(admin.TabularInline):
    model = Invitation
    extra = 0
    readonly_fields = ['created_by', 'sent_to', 'status', 'created_at', 'updated_at']
    can_delete = True
    verbose_name = _('Invitation')
    verbose_name_plural = _('Invitations')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    def member_count(self, obj):
        return obj.members.count()

    member_count.short_description = _('Member count')

    list_display = ['id', 'name', 'created_by', 'member_count', 'created_at']
    list_filter = ['created_by']
    search_fields = ['name', 'created_by__email']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['members']
    inlines = [InvitationInline]

    fieldsets = (
        (_('Info'), {'fields': ['name', 'description']}),
        (_('Created By'), {'fields': ['created_by']}),
        (_('Members'), {'fields': ['members']}),
        (_('Timestamps'), {'fields': ['created_at', 'updated_at']}),
    )


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['id', 'team', 'sent_to', 'created_by', 'status', 'created_at']
    list_filter = ['status', 'team']
    search_fields = ['team__name', 'sent_to', 'created_by']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (_('Info'), {'fields': ['team', 'sent_to', 'created_by']}),
        (_('Status'), {'fields': ['status']}),
        (_('Timestamps'), {'fields': ['created_at', 'updated_at']}),
    )
