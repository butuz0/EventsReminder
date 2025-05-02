from .models import RegistrationCard
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View


class IsOwner(permissions.BasePermission):
    '''
    Custom permission to only allow creator of the registration card to access it.
    '''
    def has_object_permission(self, request: Request, view: View, obj: RegistrationCard) -> bool:
        return obj.created_by == request.user
