from django.urls import path
from .views import (
    RegistrationCardListCreateAPIView,
    RegistrationCardAPIView
)

urlpatterns = [
    path('', RegistrationCardListCreateAPIView.as_view(), 
         name='registration-card-list-create'),
    path('<uuid:id>/', RegistrationCardAPIView.as_view(), 
         name='registration-card-retrieve-update'),
]
