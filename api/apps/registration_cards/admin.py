from django.contrib import admin
from .models import RegistrationCard

MASKED_FIELDS = [
    ('full_name', 'Applicant Full Name'),
    ('id_number', 'ID Number'),
    ('keyword_phrase', 'Keyword Phrase'),
    ('voice_phrase', 'Voice Phrase'),
    ('electronic_seal_name', 'Electronic Seal Name'),
    ('electronic_seal_keyword_phrase', 'Electronic Seal Keyword Phrase'),
]

def generate_masked_method(field_name, verbose_name):
    def _masked(self, obj):
        value = getattr(obj, field_name)
        if value:
            return f'{value[:1]}***{value[-1:]}' if len(value) >= 4 else '***'
        return 'N/A'
    _masked.short_description = verbose_name
    _masked.__name__ = f'masked_{field_name}'
    return _masked


@admin.register(RegistrationCard)
class RegistrationCardAdmin(admin.ModelAdmin):
    
    list_display = ['organization_name', 'edrpou_code', 'region', 'city']
    search_fields = ['organization_name', 'edrpou_code']
    list_filter = ['region', 'city', 'created_at']
    readonly_fields = [
        'organization_name', 'edrpou_code', 'region', 
        'city', 'email', 'phone_number', 'created_by', 
        'created_at', 'updated_at',
    ] + [f'masked_{field}' for field, _ in MASKED_FIELDS]

    fieldsets = (
        ('Legal Entity', {'fields': (
            'organization_name', 'edrpou_code', 'region', 'city'
        )}),
        ('Applicant', {'fields': (
            'masked_full_name', 'masked_id_number', 'masked_keyword_phrase', 'masked_voice_phrase'
        )}),
        ('Contacts', {'fields': ('email', 'phone_number')}),
        ('Electronic Seal', {'fields': (
            'masked_electronic_seal_name', 'masked_electronic_seal_keyword_phrase'
        )}),
        ('Metadata', {'fields': ('created_by', 'created_at', 'updated_at')}),
    )

for field_name, verbose_name in MASKED_FIELDS:
    setattr(RegistrationCardAdmin, f'masked_{field_name}', generate_masked_method(field_name, verbose_name))
