from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Profile


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

    fieldsets = (
        (_('Personal Information'), {'fields': ['user', 'gender']}),
        (_('Position'), {'fields': ['department', 'position']}),
        (_('Contacts'), {'fields': ['phone_number']}),
        (_('Social Contacts'), {'fields': ['telegram_username', 'telegram_phone_number']}),
    )


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = 'Profile'
