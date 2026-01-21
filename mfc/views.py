from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.utils.timezone import now
from django.shortcuts import render

from .models import Office, Service, Appointment
from .serializers import (
    OfficeSerializer,
    ServiceSerializer,
    AppointmentSerializer
)
from .filters import AppointmentFilter


class StandardPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'


class OfficeViewSet(viewsets.ModelViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer
    pagination_class = StandardPagination


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    pagination_class = StandardPagination
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    pagination_class = StandardPagination
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter
    ]
    filterset_class = AppointmentFilter
    search_fields = ['full_name', 'email']


    @action(methods=['GET'], detail=False)
    def today(self, request):
        today = now().date()
        qs = self.queryset.filter(
            appointment_date__date=today
        )
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

def home(request):
    return render(request, 'mfc/home.html')