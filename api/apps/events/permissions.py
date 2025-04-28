from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.views import View
from .models import Event

User = get_user_model()


class IsOwner(permissions.BasePermission):
    '''
    Custom permission to allow only owners of an event to edit it.
    '''
    def has_object_permission(self, request: Request, view: View, obj: Event) -> bool:
        user = request.user
        if user.is_superuser or user.is_staff:
            return True
        
        if user == obj.created_by:
            return True

        raise PermissionDenied('You do not have permission to edit or delete this event.')


class IsOwnerOrAssignedTo(permissions.BasePermission):
    '''
    Custom permission to allow owners of an event 
    and users assigned to the event to view it.
    '''
    def has_object_permission(self, request: Request, view: View, obj: Event) -> bool:
        user = request.user
        if user.is_superuser or user.is_staff:
            return True
        
        if user == obj.created_by or obj.assigned_to.filter(id=user.id).exists():
            return True
        
        raise PermissionDenied('You do not have permission to view this event.')
