from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from apps.common.renderers import JSONRenderer
from .models import Profile
from .serializers import ProfileSerializer, ProfileUpdateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

User = get_user_model()


class ProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['gender', 'department', 'department__faculty']
    search_fields = ['user__first_name', 'user__last_name', 'position']
    renderer_classes = [JSONRenderer]
    object_label = 'profiles'

    def get_queryset(self):
        return (self.queryset
                .exclude(user__is_staff=True)
                .exclude(user__is_superuser=True))


class ProfileDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    renderer_classes = [JSONRenderer]
    object_label = 'profile'
    lookup_field = 'user__id'
    lookup_url_kwarg = 'user_id'

    def get_queryset(self):
        return Profile.objects.select_related('user').all()


class MyProfileAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    renderer_classes = [JSONRenderer]
    object_label = 'profile'

    def get_object(self) -> Profile:
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile


class ProfileUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    renderer_classes = [JSONRenderer]
    object_label = 'profile'

    def get_object(self) -> Profile:
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile
