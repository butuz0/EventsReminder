from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import magic


def validate_image_type(value, allowed_types=None):
    allowed_types = allowed_types or ['image/jpeg', 'image/png', 'image/gif']
    mime_type = magic.Magic(mime=True).from_buffer(value.read(2048))

    if mime_type not in allowed_types:
        raise ValidationError(
            _(f'Це розширення файлу не підтримується: {mime_type}. Ваше зображення повинно мати один із таких розширень: {", ".join(allowed_types)}.'))


def validate_image_size(value, max_size_mb=5):
    max_bytes = max_size_mb * 1024 * 1024
    if value.size > max_bytes:
        raise ValidationError(_(f'Файл занадто великий. Максимальний розмір: {max_size_mb}MB.'))


def image_validator(allowed_types=None, max_size_mb=5):
    def _validator(value):
        validate_image_type(value, allowed_types)
        validate_image_size(value, max_size_mb)

    return _validator
