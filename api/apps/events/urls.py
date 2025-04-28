from django.urls import path
from .views import (
    MyEventsListAPIView, 
    EventDetailAPIView, 
    EventCreateAPIView, 
    EventUpdateAPIView, 
    EventDeleteAPIView, 
    EventLeaveAPIView
)

urlpatterns = [
    path('', MyEventsListAPIView.as_view(), name='my-events-list'),
    path('<uuid:id>/', EventDetailAPIView.as_view(), name='event-detail'),
    path('create/', EventCreateAPIView.as_view(), name='event-create'),
    path('update/<uuid:id>/', EventUpdateAPIView.as_view(), name='event-update'),
    path('delete/<uuid:id>/', EventDeleteAPIView.as_view(), name='event-delete'),
    path('leave/<uuid:id>/', EventLeaveAPIView.as_view(), name='event-leave'),
]
