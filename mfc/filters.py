import django_filters
from .models import Appointment


class AppointmentFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(
        field_name='appointment_date',
        lookup_expr='gte'
    )
    date_to = django_filters.DateFilter(
        field_name='appointment_date',
        lookup_expr='lte'
    )
    service = django_filters.NumberFilter(
        field_name='service__id'
    )
    office = django_filters.NumberFilter(
        field_name='service__office__id'
    )
    full_name = django_filters.CharFilter(
        field_name='full_name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Appointment
        fields = []

