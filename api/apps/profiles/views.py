from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.conf import settings
from apps.common.renderers import JSONRenderer
from .models import Profile, TelegramData
from .serializers import ProfileRetrieveSerializer, ProfileUpdateSerializer, ProfileSetupSerializer
from .tasks import send_telegram_greeting
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
import hashlib
import hmac
import time

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
    def post(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)

        serializer = ProfileSetupSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile set up successfully'},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TelegramAuthAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Method for authorizing Telegram user.
        Telegram Login Widget sends id, first_name, last_name,
        username, photo_url, auth_date and hash fields.
        """
        data = request.data

        received_hash = data.get('hash')
        if not received_hash:
            return Response({'detail': 'Hash missing'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Data-check-string is a concatenation of all received fields,
        # sorted in alphabetical order, in the format key=<value> with
        # a line feed character ('\n', 0x0A) used as separator
        auth_data = {key: value for key, value in data.items() if key != 'hash'}
        data_check_string = '\n'.join(f'{k}={auth_data[k]}' for k in sorted(auth_data))

        # SHA256 hash of the bot's token used as a secret key
        secret_key = hashlib.sha256(settings.TELEGRAM_BOT_TOKEN.encode()).digest()

        # hexadecimal representation of the HMAC-SHA-256
        # signature of the data-check-string
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

        # verify received hash
        if not hmac.compare_digest(received_hash, calculated_hash):
            return Response({'detail': 'Invalid Telegram auth data'},
                            status=status.HTTP_403_FORBIDDEN)

        # check auth_date expiration (10 min)
        auth_date = int(data.get('auth_date', 0))
        if now().timestamp() - auth_date > 600:
            return Response({'detail': 'Telegram auth data expired'},
                            status=status.HTTP_403_FORBIDDEN)

        # update TelegramData model
        profile = request.user.profile
        telegram_data, _ = TelegramData.objects.get_or_create(profile=profile)

        send_telegram_greeting.delay(data.get('id'))

        telegram_data.telegram_user_id = data.get('id')
        telegram_data.telegram_username = data.get('username')
        telegram_data.telegram_first_name = data.get('first_name')
        telegram_data.telegram_last_name = data.get('last_name')
        telegram_data.save()

        return Response({'detail': 'Telegram account connected successfully'})
