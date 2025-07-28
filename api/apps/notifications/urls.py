from django.urls import path
from .views import (
    NotificationByUserListAPIView,
    NotificationByObjectListAPIView,
    NotificationListCreateAPIView,
    NotificationDeleteAPIView
)

urlpatterns = [
    path('', NotificationByUserListAPIView.as_view(), name='user-notification'),
    path('create/', NotificationListCreateAPIView.as_view(), name='notifications-create'),
    path('object/<uuid:obj_id>/', NotificationByObjectListAPIView.as_view(), name='object-notifications'),
    path('delete/<int:id>/', NotificationDeleteAPIView.as_view(), name='notification-delete'),
]
