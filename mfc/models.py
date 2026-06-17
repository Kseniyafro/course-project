from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from simple_history.models import HistoricalRecords


class Office(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    is_active = models.BooleanField(default=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Service(models.Model):
    office = models.ForeignKey(
        Office,
        on_delete=models.CASCADE,
        related_name='services'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration_minutes = models.PositiveIntegerField()

    history = HistoricalRecords()

    def __str__(self):
        return self.title


class Appointment(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    appointment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.full_name} — {self.service.title}'

    def clean(self):
        super().clean()
        
        # 1. Запрет записи на прошедшее время
        if self.appointment_date and self.appointment_date < timezone.now():
            raise ValidationError({
                'appointment_date': 'Нельзя записаться на прошедшую дату и время.'
            })

        # 2. Проверка занятости временного слота для этой конкретной услуги
        overlapping = Appointment.objects.filter(
            service=self.service,
            appointment_date=self.appointment_date
        )
        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)
            
        if overlapping.exists():
            raise ValidationError({
                'appointment_date': 'Данное время для этой услуги уже занято.'
            })

        # 3. Ограничение: один активный талон на конкретную услугу по одному Email
        duplicate_email = Appointment.objects.filter(
            email=self.email,
            service=self.service,
            appointment_date__gte=timezone.now()
        )
        if self.pk:
            duplicate_email = duplicate_email.exclude(pk=self.pk)

        if duplicate_email.exists():
            raise ValidationError({
                'email': 'Вы уже записаны на эту услугу на ближайшее время.'
            })

    def save(self, *args, **kwargs):
        # Принудительно вызываем clean() перед сохранением для работы валидации в админке
        self.full_clean()
        super().save(*args, **kwargs)