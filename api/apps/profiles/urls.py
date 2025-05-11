from django.urls import path
from .views import (
    ProfileListAPIView,
    ProfileDetailAPIView,
    MyProfileAPIView,
    ProfileUpdateAPIView,
    ProfileSetupView
)

urlpatterns = [
    path('', ProfileListAPIView.as_view(), name='profile-list'),
    path('<uuid:user_id>/', ProfileDetailAPIView.as_view(), name='profile-detail'),
    path('my-profile/', MyProfileAPIView.as_view(), name='my-profile'),
    path('my-profile/setup/', ProfileSetupView.as_view(), name='my-profile-setup'),
    path('my-profile/update/', ProfileUpdateAPIView.as_view(), name='profile-update'),
]
