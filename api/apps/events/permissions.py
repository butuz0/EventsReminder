from .models import Event
from apps.common.permissions import IsAdminPermissionMixin
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View


class IsOwner(IsAdminPermissionMixin, permissions.BasePermission):
    '''
    Custom permission to allow only owners of an event to edit it.
    '''
    message = 'You do not have permission to edit or delete this event.'
    
    def has_object_permission(self, request: Request, view: View, obj: Event) -> bool:
        user = request.user
        return user == obj.created_by or self.is_admin(request)


class IsOwnerOrAssignedTo(IsAdminPermissionMixin, permissions.BasePermission):
    '''
    Custom permission to allow owners of an event 
    and users assigned to the event to view it.
    '''
    def has_object_permission(self, request: Request, view: View, obj: Event) -> bool:
        user = request.user
        return user == obj.created_by or obj.assigned_to.filter(id=user.id).exists() or self.is_admin(request)
