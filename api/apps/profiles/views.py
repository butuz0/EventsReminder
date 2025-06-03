from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from apps.common.renderers import JSONRenderer
from .models import Profile
from .serializers import ProfileRetrieveSerializer, ProfileUpdateSerializer, ProfileSetupSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

User = get_user_model()


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileRetrieveSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['department', 'department__faculty']
    search_fields = ['user__first_name', 'user__last_name', 'position']
    renderer_classes = [JSONRenderer]
    object_label = 'profiles'

    def get_queryset(self):
        return (self.queryset
                .exclude(user=self.request.user)
                .exclude(user__is_staff=True)
                .exclude(user__is_superuser=True))


class ProfileDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileRetrieveSerializer
    renderer_classes = [JSONRenderer]
    object_label = 'profile'
    lookup_field = 'user__id'
    lookup_url_kwarg = 'user_id'

    def get_queryset(self):
        return Profile.objects.select_related('user', 'telegram', 'department__faculty')


class MyProfileAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileRetrieveSerializer
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


class ProfileSetupView(APIView):
    def put(self, request):
        profile = request.user.profile

        serializer = ProfileSetupSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile set up successfully'},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
