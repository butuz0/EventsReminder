from .models import Notification
from apps.common.permissions import IsAdminPermissionMixin
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View


class IsOwner(IsAdminPermissionMixin, permissions.BasePermission):
    """
    Custom permission to allow only owners of the notification to access them.
    """
    message = 'У Вас немає доступу до цього нагадування.'

    def has_object_permission(self, request: Request, view: View, obj: Notification) -> bool:
        user = request.user
        return user == obj.created_by or self.is_admin(request)
