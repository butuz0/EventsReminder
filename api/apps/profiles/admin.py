from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Profile, TelegramData


@admin.register(TelegramData)
class TelegramDataAdmin(admin.ModelAdmin):
    list_display = ['profile', 'telegram_username', 'telegram_phone_number']
    list_display_links = ['profile', 'telegram_username']
    list_filter = ['is_verified']
    readonly_fields = ['telegram_user_id', 'telegram_chat_id', 'created_at', 'updated_at']


class TelegramDataInline(admin.StackedInline):
    model = TelegramData
    can_delete = False
    extra = 0
    verbose_name = 'Telegram Data'
    verbose_name_plural = 'Telegram Data'
    readonly_fields = ['telegram_user_id', 'telegram_chat_id', 'created_at', 'updated_at']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):  
    def user_email(self, obj: Profile) -> str:
        return obj.user.email
    user_email.short_description = _('Email')
    
    def user_faculty(self, obj: Profile) -> str:
        return obj.department.faculty.faculty_abbreviation
    user_faculty.short_description = _('Faculty')
    
    
    list_display = ['id', 'user', 'gender', 'department', 'position', 'user_email', 'phone_number']
    list_display_links = ['id', 'user']
    list_filter = ['department']
    search_fields = ['position']
    autocomplete_fields = ['department']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [TelegramDataInline]

    fieldsets = (
        (_('Personal Information'), {'fields': ['user', 'gender']}),
        (_('Position'), {'fields': ['department', 'position']}),
        (_('Contacts'), {'fields': ['phone_number']}),
        (_('Dates'), {'fields': ['created_at', 'updated_at']}),
    )


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = 'Profile'
