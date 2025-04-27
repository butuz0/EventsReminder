from django.urls import path
from .views import CustomTokenObtainPairView, CustomTokenRefreshView, LogoutAPIView


urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view()),
    path('refresh/', CustomTokenRefreshView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
]
