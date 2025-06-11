from apps.common.renderers import JSONRenderer
from .models import RegistrationCard
from .serializers import RegistrationCardSerializer
from .permissions import IsOwner
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class RegistrationCardListCreateAPIView(generics.ListCreateAPIView):
    queryset = RegistrationCard.objects.all()
    serializer_class = RegistrationCardSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    object_label = 'registration_cards'

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


class RegistrationCardAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RegistrationCard.objects.all()
    serializer_class = RegistrationCardSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'id'
