from django.db import models
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
