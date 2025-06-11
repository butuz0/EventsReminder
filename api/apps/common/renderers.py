from django.utils.translation import gettext_lazy as _
from rest_framework.renderers import JSONRenderer as BaseJSONRenderer
from typing import Any, Optional
import json


class JSONRenderer(BaseJSONRenderer):
    '''
    Modifies the structure of rendered JSON response by
    adding status_code and wrapping data in object_label key.
    '''
    charset = 'utf-8'
    object_label = 'object'

    def render(self, data: Any, accepted_media_type: Optional[str], renderer_context: Optional[dict]) -> bytes:
        context = renderer_context or {}

        view = context.get('view')

        object_label = getattr(view, 'object_label', self.object_label)

        response = context.get('response')

        if not response:
            raise ValueError(_('Response not found in renderer context.'))

        status_code = response.status_code
        errors = data.get('errors', None)

        if errors is not None:
            return super().render(data, accepted_media_type, renderer_context)

        return json.dumps({'status_code': status_code, object_label: data}).encode(self.charset)
