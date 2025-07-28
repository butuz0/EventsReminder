from apps.common.renderers import JSONRenderer
from .models import Notification
from .serializers import NotificationSerializer
from .permissions import IsOwner
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class NotificationListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to create notifications.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    object_label = 'notifications'


class BaseNotificationDetailAPIView(generics.ListAPIView):
    """
    API view to retrieve notifications.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    renderer_classes = [JSONRenderer]
    object_label = 'notifications'


class NotificationByObjectListAPIView(BaseNotificationDetailAPIView):
    """
    API view to retrieve notifications for any allowed models instance by obj_id.
    """

    def get_queryset(self):
        obj_id = self.kwargs.get('obj_id', None)
        user = self.request.user
        return (self.queryset
                .filter(created_by=user,
                        object_id=obj_id)
                .order_by('notification_datetime'))


class NotificationByUserListAPIView(BaseNotificationDetailAPIView):
    """
    API view to retrieve notifications by user_id.
    """

    def get_queryset(self):
        user = self.request.user
        return (self.queryset
                .filter(created_by=user)
                .order_by('notification_datetime'))


class NotificationDeleteAPIView(generics.DestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'id'
