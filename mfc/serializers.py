from rest_framework import serializers
from django.utils import timezone
from .models import Office, Service, Appointment


class OfficeSerializer(serializers.ModelSerializer):
    # 5️⃣ Выводим аннотированное поле (количество услуг в офисе), посчитанное во views.py
    total_services = serializers.IntegerField(read_only=True)

    class Meta:
        model = Office
        fields = ['id', 'name', 'address', 'is_active', 'total_services']


class ServiceSerializer(serializers.ModelSerializer):
    # 5️⃣ Выводим аннотированное поле (количество записей на услугу), посчитанное во views.py
    total_appointments = serializers.IntegerField(read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'office', 'title', 'description', 'duration_minutes', 'total_appointments']


class AppointmentSerializer(serializers.ModelSerializer):
    # 4.1️⃣ Использование SerializerMethodField (выводим название офиса через метод)
    office_name = serializers.SerializerMethodField()
    
    # 4.2️⃣ Поле для демонстрации передачи данных в сериализатор через контекст
    notification_banner = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            'id', 'service', 'full_name', 'email', 
            'appointment_date', 'created_at', 'office_name', 'notification_banner'
        ]

    # Логика для SerializerMethodField (Пункт 4.1)
    def get_office_name(self, obj):
        # Благодаря select_related во views.py этот метод не делает дополнительных SQL-запросов
        return obj.service.office.name

    # Логика для извлечения данных из контекста view (Пункт 4.2)
    def get_notification_banner(self, obj):
        # Забираем кастомную строку, которую передали во ViewSet через get_serializer_context
        return self.context.get('banner_text', 'Добро пожаловать в МФЦ!')

    # ✅ Твоя бизнес-валидация даты (Пункт 2)
    def validate_appointment_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                'Нельзя записаться на прошедшую дату'
            )
        return value

    # ✅ Комплексная бизнес-валидация на пересечение слотов и дубликаты (Пункт 2)
    def validate(self, attrs):
        service = attrs.get('service')
        appointment_date = attrs.get('appointment_date')
        email = attrs.get('email')
        
        # Определяем, это создание новой записи или обновление существующей (чтобы исключить её из проверки)
        request = self.context.get('request')
        instance_id = request.parser_context['kwargs'].get('pk') if request else None

        # 1. Проверка занятости временного слота для этой конкретной услуги
        overlapping_slots = Appointment.objects.filter(
            service=service,
            appointment_date=appointment_date
        )
        if instance_id:
            overlapping_slots = overlapping_slots.exclude(pk=instance_id)
            
        if overlapping_slots.exists():
            raise serializers.ValidationError({
                'appointment_date': 'Данное время для этой услуги уже занято другим заявителем.'
            })

        # 2. Ограничение «Один активный талон на услугу по одному Email»
        duplicate_emails = Appointment.objects.filter(
            email=email,
            service=service,
            appointment_date__gte=timezone.now()
        )
        if instance_id:
            duplicate_emails = duplicate_emails.exclude(pk=instance_id)

        if duplicate_emails.exists():
            raise serializers.ValidationError({
                'email': 'Вы уже записаны на эту услугу. Нельзя плодить дублирующие талоны.'
            })

        return attrs

