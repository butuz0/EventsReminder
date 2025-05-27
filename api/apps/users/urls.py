from django.urls import path, include
from .views import CustomTokenObtainPairView, CustomTokenRefreshView, LogoutAPIView, CustomUserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view()),
    path('refresh/', CustomTokenRefreshView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('', include(router.urls)),
]
