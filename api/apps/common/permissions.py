from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsAdminPermissionMixin:
    '''
    Mixin to allow admin users to access data.
    '''
    def is_admin(self, request: Request) -> bool:
        user = request.user
        return user and (user.is_superuser or user.is_staff)
