import django_filters
from .models import Appointment


class AppointmentFilter(django_filters.FilterSet):
    # Фильтрация записей «с определенной даты» (больше или равно)
    date_from = django_filters.DateFilter(
        field_name='appointment_date',
        lookup_expr='gte'
    )
    # Фильтрация записей «по определенную дату» (меньше или равно)
    date_to = django_filters.DateFilter(
        field_name='appointment_date',
        lookup_expr='lte'
    )
    # Фильтр по ID конкретной услуги
    service = django_filters.NumberFilter(
        field_name='service__id'
    )
    # Фильтр по ID офиса (проходит сквозь связь услуги к офису)
    office = django_filters.NumberFilter(
        field_name='service__office__id'
    )
    # Поиск по ФИО заявителя (без учета регистра и по частичному совпадению)
    full_name = django_filters.CharFilter(
        field_name='full_name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Appointment
        fields = []  # Все используемые поля мы объявили явно выше