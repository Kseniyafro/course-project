from rest_framework import serializers
from django.utils import timezone
from .models import Office, Service, Appointment


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    # ✅ бизнес-валидация
    def validate_appointment_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                'Нельзя записаться на прошедшую дату'
            )
        return value

