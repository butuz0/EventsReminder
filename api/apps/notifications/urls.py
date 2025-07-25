from django.urls import path
from .views import (
    NotificationByUserListAPIView,
    NotificationByEventListAPIView,
    NotificationListCreateAPIView,
    NotificationDeleteAPIView
)

urlpatterns = [
    path('', NotificationByUserListAPIView.as_view(), name='user-notification'),
    path('create/', NotificationListCreateAPIView.as_view(), name='notifications-create'),
    path('event/<uuid:event_id>/', NotificationByEventListAPIView.as_view(), name='event-notifications'),
    path('delete/<int:id>/', NotificationDeleteAPIView.as_view(), name='notification-delete'),
]
