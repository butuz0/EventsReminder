from apps.common.permissions import IsAdminPermissionMixin
from .models import Team
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View


class IsOwner(IsAdminPermissionMixin, permissions.BasePermission):
    '''
    Custom permission to allow only owners of the team to modify it.
    '''
    message = 'You do not have permission to modify this team.'
    
    def has_object_permission(self, request: Request, view: View, obj: Team) -> bool:
        user = request.user
        return user == obj.created_by or self.is_admin(request)


class IsOwnerOrMember(IsAdminPermissionMixin, permissions.BasePermission):
    '''
    Custom permission to allow only owners or members of the team view it.
    '''
    message = 'You do not have permission to view this team.'
    
    def has_object_permission(self, request: Request, view: View, obj: Team) -> bool:
        user = request.user
        return user == obj.created_by or obj.members.filter(id=user.id).exists() or self.is_admin(request)
