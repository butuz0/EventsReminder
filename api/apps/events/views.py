from django.shortcuts import get_object_or_404
from apps.common.renderers import JSONRenderer
from .models import Event
from .serializers import EventSerializer
from .permissions import IsOwner, IsOwnerOrAssignedTo
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class MyEventsListAPIView(generics.ListAPIView):
    '''
    API view to retrieve a list of events created by 
    or assigned to the authenticated user.
    '''
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAssignedTo]
    pagination_class = StandardResultsSetPagination
    renderer_classes = [JSONRenderer]
    object_label = 'events'

    def get_queryset(self):
        created_events = Event.objects.filter(created_by=self.request.user)
        assigned_events = Event.objects.filter(assigned_to=self.request.user)
        return (created_events | assigned_events).distinct().order_by('-start_datetime')


class EventDetailAPIView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAssignedTo]
    renderer_classes = [JSONRenderer]
    object_label = 'event'
    lookup_field = 'id'


class EventCreateAPIView(generics.CreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    object_label = 'event'


class EventUpdateAPIView(generics.UpdateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    renderer_classes = [JSONRenderer]
    object_label = 'event'
    lookup_field = 'id'

    def get_queryset(self):
        return Event.objects.filter(created_by=self.request.user)


class EventDeleteAPIView(generics.DestroyAPIView):
    '''
    API view to delete an event created by the user.
    '''
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'id'

    def get_queryset(self):
        return Event.objects.filter(created_by=self.request.user)


class EventLeaveAPIView(APIView):
    '''
    API view to delete youself from assigned_to field of an event.
    '''
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id):
        event = get_object_or_404(Event, id=id)

        if event.assigned_to.filter(id=request.user.id).exists():
            event.assigned_to.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)

        raise PermissionDenied('You cannot leave the event because you have never been assigned to it.')
