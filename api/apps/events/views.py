from django.shortcuts import get_object_or_404
from apps.common.renderers import JSONRenderer
from .models import Event, RecurringEvent
from .serializers import (
    EventCreateSerializer,
    EventUpdateSerializer,
    EventDetailSerializer,
    RecurringEventSerializer
)
from .permissions import IsOwner, IsOwnerOrAssignedTo
from .filters import EventFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, filters as drf_filters
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
    queryset = Event.objects.all().prefetch_related('tags', 'assigned_to')
    serializer_class = EventDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAssignedTo]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter]
    filterset_class = EventFilter
    search_fields = ['title', 'description', 'location', 'tags__name']
    renderer_classes = [JSONRenderer]
    object_label = 'events'

    def get_queryset(self):
        created_events = Event.objects.filter(created_by=self.request.user)
        assigned_events = Event.objects.filter(assigned_to=self.request.user)
        return (created_events | assigned_events).distinct().order_by('start_datetime')


class EventDetailAPIView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAssignedTo]
    renderer_classes = [JSONRenderer]
    object_label = 'event'
    lookup_field = 'id'


class EventCreateAPIView(generics.CreateAPIView):
    serializer_class = EventCreateSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    object_label = 'event'


class EventUpdateAPIView(generics.UpdateAPIView):
    serializer_class = EventUpdateSerializer
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
    serializer_class = EventUpdateSerializer
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


class RecurringEventCreateAPIView(generics.CreateAPIView):
    serializer_class = RecurringEventSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    object_label = 'recurring_event'

    def perform_create(self, serializer):
        event_id = self.kwargs['event_id']
        event = Event.objects.get(id=event_id)

        if event.created_by != self.request.user:
            raise PermissionDenied('Only event creator can create a recurring event.')

        event.is_recurring = True
        event.save(update_fields=['is_recurring'])

        serializer.save(event=event)


class RecurringEventUpdateAPIView(generics.UpdateAPIView):
    queryset = RecurringEvent.objects.all()
    serializer_class = RecurringEventSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    renderer_classes = [JSONRenderer]
    object_label = 'recurring_event'

    def get_object(self):
        event_id = self.kwargs['event_id']
        event = get_object_or_404(Event, id=event_id)
        return get_object_or_404(RecurringEvent, event=event)
