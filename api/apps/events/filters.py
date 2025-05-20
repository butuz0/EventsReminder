from taggit.models import Tag
from .models import Event
import django_filters


class EventFilter(django_filters.FilterSet):
    from_date = django_filters.DateTimeFilter(field_name='start_datetime',
                                              lookup_expr='gte')
    to_date = django_filters.DateTimeFilter(field_name='start_datetime',
                                            lookup_expr='lte')

    priority = django_filters.NumberFilter(field_name='priority')

    tags = django_filters.ModelMultipleChoiceFilter(field_name='tags__name',
                                                    to_field_name='name',
                                                    queryset=Tag.objects.all(),
                                                    lookup_expr='icontains')

    is_recurring = django_filters.BooleanFilter(field_name='is_recurring')

    team = django_filters.UUIDFilter(field_name='team__id')

    ordering = django_filters.OrderingFilter(
        fields=(
            ('start_datetime', 'start'),
            ('-start_datetime', 'start_desc'),
            ('priority', 'priority'),
            ('-priority', 'priority_desc'),
            ('title', 'title'),
            ('-title', 'title_desc'),
        )
    )

    class Meta:
        model = Event
        fields = ['priority', 'tags', 'from_date', 'to_date', 'is_recurring', 'team']
